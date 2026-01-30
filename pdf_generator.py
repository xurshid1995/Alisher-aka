# -*- coding: utf-8 -*-
"""
PDF Generator - Savdo cheklari uchun
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

def generate_sale_receipt_pdf(
    sale_data: dict,
    output_path: str = None
) -> str:
    """
    Savdo cheki PDF yaratish
    
    Args:
        sale_data: Savdo ma'lumotlari
        output_path: PDF saqlash yo'li (agar None bo'lsa, temp file yaratiladi)
    
    Returns:
        str: PDF fayl yo'li
    """
    if output_path is None:
        output_path = f"/tmp/sale_{sale_data['sale_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # PDF yaratish
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Y pozitsiyasi
    y = height - 30*mm
    
    # Sarlavha
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, "SAVDO CHEKI")
    y -= 10*mm
    
    # Chiziq
    c.line(30*mm, y, width-30*mm, y)
    y -= 10*mm
    
    # Asosiy ma'lumotlar
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, y, f"Check #: {sale_data['sale_id']}")
    y -= 7*mm
    
    c.drawString(30*mm, y, f"Sana: {sale_data['date']}")
    y -= 7*mm
    
    if sale_data.get('customer_name'):
        c.drawString(30*mm, y, f"Mijoz: {sale_data['customer_name']}")
        y -= 7*mm
    
    c.drawString(30*mm, y, f"Do'kon: {sale_data['location']}")
    y -= 10*mm
    
    # Mahsulotlar jadvali
    c.line(30*mm, y, width-30*mm, y)
    y -= 7*mm
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30*mm, y, "Mahsulot")
    c.drawString(120*mm, y, "Soni")
    c.drawString(145*mm, y, "Narx")
    c.drawString(170*mm, y, "Jami")
    y -= 5*mm
    
    c.line(30*mm, y, width-30*mm, y)
    y -= 7*mm
    
    # Mahsulotlar ro'yxati
    c.setFont("Helvetica", 9)
    for item in sale_data.get('items', []):
        # Mahsulot nomi (uzun bo'lsa qisqartirish)
        product_name = item['name'][:40]
        c.drawString(30*mm, y, product_name)
        c.drawRightString(135*mm, y, f"{item['quantity']}")
        c.drawRightString(165*mm, y, f"{item['unit_price']:,.0f}")
        c.drawRightString(190*mm, y, f"{item['total']:,.0f}")
        y -= 6*mm
        
        if y < 40*mm:  # Sahifa tugashidan oldin
            c.showPage()
            y = height - 30*mm
            c.setFont("Helvetica", 9)
    
    y -= 5*mm
    c.line(30*mm, y, width-30*mm, y)
    y -= 10*mm
    
    # Jami summa
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, y, "JAMI:")
    c.drawRightString(190*mm, y, f"{sale_data['total_amount']:,.0f} so'm")
    y -= 8*mm
    
    # To'lov ma'lumotlari
    if sale_data.get('paid_amount', 0) > 0:
        c.setFont("Helvetica", 10)
        c.drawString(30*mm, y, "To'langan:")
        c.drawRightString(190*mm, y, f"{sale_data['paid_amount']:,.0f} so'm")
        y -= 6*mm
        
        # To'lov turlari
        if sale_data.get('cash', 0) > 0:
            c.drawString(35*mm, y, "Naqd:")
            c.drawRightString(190*mm, y, f"{sale_data['cash']:,.0f} so'm")
            y -= 6*mm
        if sale_data.get('click', 0) > 0:
            c.drawString(35*mm, y, "Click:")
            c.drawRightString(190*mm, y, f"{sale_data['click']:,.0f} so'm")
            y -= 6*mm
        if sale_data.get('terminal', 0) > 0:
            c.drawString(35*mm, y, "Terminal:")
            c.drawRightString(190*mm, y, f"{sale_data['terminal']:,.0f} so'm")
            y -= 6*mm
    
    # Qarz
    if sale_data.get('debt', 0) > 0:
        y -= 2*mm
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.red)
        c.drawString(30*mm, y, "QARZ:")
        c.drawRightString(190*mm, y, f"{sale_data['debt']:,.0f} so'm")
        c.setFillColor(colors.black)
        y -= 8*mm
    
    # Footer
    y -= 10*mm
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, y, "Xaridingiz uchun rahmat!")
    y -= 5*mm
    c.drawCentredString(width/2, y, f"Tel: {sale_data.get('phone', '')}")
    
    # PDF ni saqlash
    c.save()
    
    return output_path
