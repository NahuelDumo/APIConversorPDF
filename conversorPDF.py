import asyncio
from playwright.async_api import async_playwright, TimeoutError
from PIL import Image
import os
import uuid
import tempfile

async def capturar_paginas_y_generar_pdf(html_path, output_pdf_path, page_ids):
    temp_dir = tempfile.gettempdir()
    image_paths = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1686, "height": 1205},
            device_scale_factor=4  # Doble resolución para capturas más nítidas
        )
        page = await context.new_page()
        ruta_absoluta = os.path.abspath(html_path)
        await page.goto(f"file:///{ruta_absoluta}", wait_until="networkidle")

        for pid in page_ids:
            try:
                await page.wait_for_selector(f"#{pid}", timeout=60000, state="attached")
                element = await page.query_selector(f"#{pid}")
                if element:
                    screenshot_path = os.path.join(temp_dir, f"{pid}_{uuid.uuid4()}.png")
                    await element.screenshot(path=screenshot_path)
                    image_paths.append(screenshot_path)
                else:
                    print(f"No se encontró elemento con id: {pid}")
            except TimeoutError:
                print(f"Timeout esperando el elemento con id: {pid}")

        await browser.close()

    # Convertir imágenes a PDF multipágina
    images = []
    for img_path in image_paths:
        with Image.open(img_path) as img:
            images.append(img.convert("RGB"))

    if images:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF generado en: {output_pdf_path}")
    else:
        print("No se generaron imágenes para el PDF.")

    # Limpiar imágenes temporales
    for img_path in image_paths:
        if os.path.exists(img_path):
            os.remove(img_path)

# ✅ Solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    html_input = "C:/Users/nahue/Downloads/Nº02008_presupuesto.html"
    pdf_output = "C:/Users/nahue/Downloads/presupuesto_paginas_individuales_alta_calidad.pdf"
    page_ids = ["pf1", "pf2", "pf3"]  # IDs de tus páginas

    asyncio.run(capturar_paginas_y_generar_pdf(html_input, pdf_output, page_ids))
