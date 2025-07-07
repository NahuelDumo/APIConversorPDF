from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import os
import uuid
import tempfile
import asyncio
import json
from typing import List
import uvicorn

# Importar tu función existente
from conversorPDF import capturar_paginas_y_generar_pdf

app = FastAPI(title="HTML to PDF Converter API", version="1.0.0")

@app.post("/convert-html-to-pdf")
async def convert_html_to_pdf(
    html_file: UploadFile = File(..., description="Archivo HTML a convertir"),
    page_ids: str = Form(..., description="IDs de páginas separados por comas (ej: pf1,pf2,pf3)")
):
    """
    Convierte un archivo HTML a PDF capturando elementos específicos por ID
    
    - **html_file**: Archivo HTML a procesar
    - **page_ids**: IDs de elementos a capturar, separados por comas
    """
    # Validar que el archivo sea HTML
    if not html_file.filename.endswith(('.html', '.htm')):
        raise HTTPException(status_code=400, detail="El archivo debe ser HTML")
    
    try:
        # Crear archivo temporal para el HTML
        temp_dir = tempfile.gettempdir()
        html_temp_path = os.path.join(temp_dir, f"temp_{uuid.uuid4()}.html")
        
        # Guardar el archivo HTML subido
        with open(html_temp_path, 'wb') as f:
            content = await html_file.read()
            f.write(content)
        
        # Procesar los IDs de página
        page_ids_list = [pid.strip() for pid in page_ids.split(',') if pid.strip()]
        
        if not page_ids_list:
            raise HTTPException(status_code=400, detail="Debe especificar al menos un ID de página")
        
        # Generar nombre único para el PDF de salida
        pdf_output_path = os.path.join(temp_dir, f"converted_{uuid.uuid4()}.pdf")
        
        # Usar tu función existente
        await capturar_paginas_y_generar_pdf(html_temp_path, pdf_output_path, page_ids_list)
        
        # Limpiar archivo HTML temporal
        if os.path.exists(html_temp_path):
            os.remove(html_temp_path)
        
        # Verificar que el PDF se generó correctamente
        if not os.path.exists(pdf_output_path):
            raise HTTPException(status_code=500, detail="Error generando el PDF")
        
        # Devolver el archivo PDF
        return FileResponse(
            pdf_output_path,
            media_type="application/pdf",
            filename=f"converted_{html_file.filename.replace('.html', '')}.pdf"
        )
        
    except Exception as e:
        # Limpiar archivos temporales en caso de error
        if 'html_temp_path' in locals() and os.path.exists(html_temp_path):
            os.remove(html_temp_path)
        if 'pdf_output_path' in locals() and os.path.exists(pdf_output_path):
            os.remove(pdf_output_path)
        
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")

@app.post("/convert-html-to-pdf-json")
async def convert_html_to_pdf_json(
    html_file: UploadFile = File(..., description="Archivo HTML a convertir"),
    config: str = Form(..., description="Configuración JSON con page_ids")
):
    """
    Convierte un archivo HTML a PDF usando configuración JSON
    
    - **html_file**: Archivo HTML a procesar
    - **config**: JSON con configuración (ej: {"page_ids": ["pf1", "pf2", "pf3"]})
    """
    # Validar que el archivo sea HTML
    if not html_file.filename.endswith(('.html', '.htm')):
        raise HTTPException(status_code=400, detail="El archivo debe ser HTML")
    
    try:
        # Parsear configuración JSON
        config_data = json.loads(config)
        page_ids_list = config_data.get("page_ids", [])
        
        if not page_ids_list:
            raise HTTPException(status_code=400, detail="Debe especificar page_ids en la configuración")
        
        # Crear archivo temporal para el HTML
        temp_dir = tempfile.gettempdir()
        html_temp_path = os.path.join(temp_dir, f"temp_{uuid.uuid4()}.html")
        
        # Guardar el archivo HTML subido
        with open(html_temp_path, 'wb') as f:
            content = await html_file.read()
            f.write(content)
        
        # Generar nombre único para el PDF de salida
        pdf_output_path = os.path.join(temp_dir, f"converted_{uuid.uuid4()}.pdf")
        
        # Usar tu función existente
        await capturar_paginas_y_generar_pdf(html_temp_path, pdf_output_path, page_ids_list)
        
        # Limpiar archivo HTML temporal
        if os.path.exists(html_temp_path):
            os.remove(html_temp_path)
        
        # Verificar que el PDF se generó correctamente
        if not os.path.exists(pdf_output_path):
            raise HTTPException(status_code=500, detail="Error generando el PDF")
        
        # Devolver el archivo PDF
        return FileResponse(
            pdf_output_path,
            media_type="application/pdf",
            filename=f"converted_{html_file.filename.replace('.html', '')}.pdf"
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Configuración JSON inválida")
    except Exception as e:
        # Limpiar archivos temporales en caso de error
        if 'html_temp_path' in locals() and os.path.exists(html_temp_path):
            os.remove(html_temp_path)
        if 'pdf_output_path' in locals() and os.path.exists(pdf_output_path):
            os.remove(pdf_output_path)
        
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")

@app.get("/")
async def root():
    """Endpoint de prueba"""
    return {"message": "HTML to PDF Converter API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)