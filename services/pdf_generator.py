import base64
import os
from datetime import datetime
from io import BytesIO

from flask import current_app
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PHOTO_MAX_WIDTH = 4.3 * cm
PHOTO_MAX_HEIGHT = 4 * cm
PHOTOS_PAR_PIECE_PDF = 3
SIGNATURE_MAX_WIDTH = 5 * cm
SIGNATURE_MAX_HEIGHT = 2.5 * cm

STYLES = getSampleStyleSheet()
STYLE_TITLE = ParagraphStyle(
    "AuditTitle", parent=STYLES["Title"], fontSize=18, textColor=colors.HexColor("#0f172a")
)
STYLE_H2 = ParagraphStyle(
    "AuditH2", parent=STYLES["Heading2"], fontSize=13, textColor=colors.HexColor("#0f172a"),
    spaceBefore=14, spaceAfter=6,
)
STYLE_BODY = ParagraphStyle("AuditBody", parent=STYLES["BodyText"], fontSize=10)
STYLE_MUTED = ParagraphStyle(
    "AuditMuted", parent=STYLES["BodyText"], fontSize=9, textColor=colors.HexColor("#64748b")
)

HEADER_BG = colors.HexColor("#0f172a")
ROW_BG = colors.HexColor("#f1f5f9")
GRID_COLOR = colors.HexColor("#cbd5e1")


def _humanize(value):
    return (value or "").replace("_", " ").capitalize()


def _oui_non(value):
    return "Oui" if value else "Non"


def _composants_table(zone):
    header = ["Composant", "Interrupteur", "Neutre", "Motorisation", "Qté", "Notes"]
    rows = [header]
    for c in zone.composants:
        rows.append(
            [
                _humanize(c.type_composant),
                _humanize(c.type_interrupteur),
                _oui_non(c.presence_neutre),
                _oui_non(c.besoin_motorisation),
                str(c.quantite or 1),
                c.notes or "-",
            ]
        )

    table = Table(rows, colWidths=[3.2 * cm, 3 * cm, 1.8 * cm, 2.3 * cm, 1.2 * cm, 4.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_BG]),
                ("GRID", (0, 0), (-1, -1), 0.5, GRID_COLOR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _photo_thumbnail(path):
    try:
        with PILImage.open(path) as img:
            largeur, hauteur = img.size
    except (OSError, ValueError):
        return None
    ratio = min(PHOTO_MAX_WIDTH / largeur, PHOTO_MAX_HEIGHT / hauteur)
    return Image(path, width=largeur * ratio, height=hauteur * ratio)


def _photos_flowable(zone, upload_folder):
    photos = zone.photos[:PHOTOS_PAR_PIECE_PDF]
    vignettes = []
    for photo in photos:
        chemin = os.path.join(upload_folder, str(zone.id), photo.filename)
        if not os.path.exists(chemin):
            continue
        vignette = _photo_thumbnail(chemin)
        if vignette:
            vignettes.append(vignette)

    if not vignettes:
        return None

    table = Table([vignettes], colWidths=[PHOTO_MAX_WIDTH] * len(vignettes))
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _signature_image(data_uri):
    if not data_uri or not data_uri.startswith("data:image/png;base64,"):
        return None
    try:
        raw = base64.b64decode(data_uri.split(",", 1)[1])
        buf = BytesIO(raw)
        with PILImage.open(buf) as img:
            largeur, hauteur = img.size
        buf.seek(0)
    except (OSError, ValueError, IndexError):
        return None
    ratio = min(SIGNATURE_MAX_WIDTH / largeur, SIGNATURE_MAX_HEIGHT / hauteur, 1)
    return Image(buf, width=largeur * ratio, height=hauteur * ratio)


def generate_projet_pdf(projet, upload_folder=None):
    """Génère le rapport d'audit complet d'un projet (toutes les pièces)."""
    if upload_folder is None:
        upload_folder = current_app.config["UPLOAD_FOLDER"]

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        title=f"Audit domotique - {projet.nom}",
    )

    story = [
        Paragraph("Rapport d'audit domotique", STYLE_TITLE),
        Paragraph(
            f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", STYLE_MUTED
        ),
        Spacer(1, 0.6 * cm),
    ]

    infos = Table(
        [
            ["Client", projet.client.nom],
            ["Contact", " · ".join(filter(None, [projet.client.telephone, projet.client.email])) or "-"],
            ["Projet", projet.nom],
            ["Adresse du chantier", projet.adresse_chantier or "-"],
            ["Statut", _humanize(projet.statut)],
        ],
        colWidths=[4 * cm, 12 * cm],
    )
    infos.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(infos)

    if not projet.zones:
        story.append(Spacer(1, 0.6 * cm))
        story.append(Paragraph("Aucune pièce auditée pour ce projet.", STYLE_BODY))

    for zone in projet.zones:
        sous_titre = _humanize(zone.type_piece)
        if zone.surface_m2:
            sous_titre += f" · {zone.surface_m2} m²"
        story.append(Paragraph(f"{zone.nom} — {sous_titre}", STYLE_H2))
        if zone.notes:
            story.append(Paragraph(zone.notes, STYLE_BODY))
            story.append(Spacer(1, 0.2 * cm))
        if zone.composants:
            story.append(_composants_table(zone))
        else:
            story.append(Paragraph("Aucun composant renseigné.", STYLE_MUTED))

        photos_flowable = _photos_flowable(zone, upload_folder)
        if photos_flowable:
            story.append(Spacer(1, 0.2 * cm))
            story.append(photos_flowable)
            if len(zone.photos) > PHOTOS_PAR_PIECE_PDF:
                reste = len(zone.photos) - PHOTOS_PAR_PIECE_PDF
                story.append(Paragraph(f"+ {reste} autre(s) photo(s) disponible(s) en ligne.", STYLE_MUTED))

        story.append(Spacer(1, 0.3 * cm))

    validation = projet.derniere_validation
    story.append(Paragraph("Validation client", STYLE_H2))
    if validation:
        story.append(
            Paragraph(
                f"Audit validé par <b>{validation.nom_signataire}</b> "
                f"le {validation.created_at.strftime('%d/%m/%Y à %H:%M')}.",
                STYLE_BODY,
            )
        )
        if validation.commentaire:
            story.append(Spacer(1, 0.15 * cm))
            story.append(Paragraph(f"Commentaire : {validation.commentaire}", STYLE_BODY))
        signature_image = _signature_image(validation.signature)
        if signature_image:
            story.append(Spacer(1, 0.2 * cm))
            story.append(Paragraph("Signature :", STYLE_MUTED))
            story.append(signature_image)
    else:
        story.append(Paragraph("Audit non encore validé par le client.", STYLE_MUTED))

    doc.build(story)
    buffer.seek(0)
    return buffer
