#!/usr/bin/env python3
"""
Eski table layout va yangi modal sistemasini birlashtirgan hybrid customer_detail.html yaratish
"""

# Eski CSS ni saqlaydiganlar (rowspan, UZS badges, va h.)
OLD_TABLE_CSS = """
    /* Barcha jadval qatorlariga bir xil balandlik */
    .sales-table tbody tr {
        height: auto;
        min-height: 28px;
    }

    .sales-table tbody td {
        padding: 4px 6px;
        line-height: 1.2;
        vertical-align: middle;
    }

    /* Rowspan ustunlari - vertical va horizontal markazlashtirilgan */
    .group-cell {
        vertical-align: middle !important;
        text-align: center !important;
        padding: 4px 6px !important;
    }

    /* Mahsulot ustuni uchun bir xil font */
    .product-cell {
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* Sana va vaqt */
    .group-datetime {
        background-color: #f8f9fa;
    }

    /* Sotuvchi */
    .group-seller {
        background-color: #f8f9fa;
    }

    /* Jami summa */
    .group-total {
        background-color: #e7f3ff;
        font-weight: 700 !important;
    }

    /* Jami foyda */
    .group-profit {
        background-color: #e8f5e9;
        font-weight: 700 !important;
    }

    /* Amallar ustuni */
    .group-actions {
        background-color: #f8f9fa;
        vertical-align: middle !important;
        text-align: center !important;
        padding: 2px !important;
    }

    .group-actions button {
        width: 100%;
        margin: 2px 0;
    }

    /* Savdo tarixi jadvali */
    .orders-section {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .orders-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
    }

    .orders-header h2 {
        margin: 0;
        font-size: 1rem;
        font-weight: 700;
    }
"""

# Yangi modal CSS
NEW_MODAL_CSS = """
    /* Sales-history.html dan modal CSS - 100% NUSXA */
    .sale-main-info {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #f8f9fa;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #007bff;
        gap: 8px;
        flex-wrap: wrap;
        text-align: center;
    }

    .customer-label {
        font-weight: 500;
        color: #6c757d;
        font-size: 16px;
    }

    .customer-name {
        font-size: 16px;
        font-weight: 600;
        color: #2c3e50;
    }

    .customer-phone {
        font-size: 16px;
        color: #6c757d;
        font-weight: 500;
    }

    .date-separator {
        font-size: 18px;
        color: #6c757d;
        margin: 0 10px;
    }

    .date-label {
        font-weight: 500;
        color: #6c757d;
        font-size: 16px;
    }

    .date-value {
        font-weight: 600;
        color: #007bff;
        font-size: 16px;
    }

    .modal-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #dee2e6;
    }

    .modal-table th,
    .modal-table td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
    }

    .modal-table th {
        background-color: #f8f9fa;
        font-weight: 600;
        color: #495057;
    }

    .modal-table td {
        color: #6c757d;
    }

    .total-info {
        background: #e9ecef;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }

    .total-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
    }

    .total-label {
        font-weight: 600;
        color: #495057;
    }

    .total-value {
        font-weight: 700;
        font-size: 16px;
    }

    .total-value.positive {
        color: #28a745;
    }

    .total-value.negative {
        color: #dc3545;
    }

    /* Modal header actions */
    .modal-header-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .btn-print {
        background: #28a745;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 5px;
        transition: background 0.2s;
    }

    .btn-print:hover {
        background: #218838;
    }

    .btn-print i {
        font-size: 12px;
    }

    .btn-excel {
        background: #17a2b8;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 5px;
        transition: background 0.2s;
        margin-left: 8px;
    }

    .btn-excel:hover {
        background: #138496;
    }

    .btn-excel i {
        font-size: 12px;
    }

    /* Savdo tafsilotlari modal - markazda ochish */
    .sale-details-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.6);
        display: flex !important;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        padding: 20px;
        box-sizing: border-box;
    }

    .sale-details-content {
        max-width: 1200px;
        width: 95%;
        max-height: 90vh;
        overflow-y: auto;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        animation: modalFadeIn 0.3s ease-out;
    }

    @keyframes modalFadeIn {
        from {
            opacity: 0;
            transform: scale(0.9) translateY(-20px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
"""

print("Python script yaratildi - hybrid customer_detail.html yaratish uchun kerakli konstanta'lar kiritildi")
print(f"OLD_TABLE_CSS uzunligi: {len(OLD_TABLE_CSS)} belglar")
print(f"NEW_MODAL_CSS uzunligi: {len(NEW_MODAL_CSS)} belglar")
