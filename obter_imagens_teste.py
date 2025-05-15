import os
import skimage.data
import skimage.io

# Diretórios para salvar as imagens de exemplo
base_path = "/home/ubuntu/trabalho_faculdade_python"
image_dirs = {
    "filtros_frequencia": os.path.join(base_path, "filtros_frequencia_python", "imagens_exemplo"),
    "segmentacao_watershed": os.path.join(base_path, "segmentacao_watershed_python", "imagens_exemplo"),
    "crescimento_regioes": os.path.join(base_path, "crescimento_regioes_python", "imagens_exemplo"),
}

# Certificar que os diretórios existem
for dir_path in image_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Imagens a serem carregadas e salvas
# Usaremos imagens diferentes para variar os exemplos, ou a mesma se aplicável
images_to_load = {
    "camera.png": skimage.data.camera(),
    "coins.png": skimage.data.coins(),
    "astronaut.png": skimage.data.astronaut(),
    "text.png": skimage.data.text(),
    "chelsea.png": skimage.data.chelsea(), # Gato para crescimento de regiões ou watershed
    "moon.png": skimage.data.moon(), # Boa para filtros de frequência
    "horse.png": skimage.data.horse(), # Imagem binária, pode ser útil para watershed/crescimento
}

# Salvar as imagens nos diretórios apropriados
# Para este exemplo, vamos salvar algumas imagens específicas em cada pasta
# ou você pode optar por salvar todas em um local comum e referenciá-las.

# Filtros de Frequência - usaremos moon e camera
skimage.io.imsave(os.path.join(image_dirs["filtros_frequencia"], "moon_original.png"), images_to_load["moon.png"])
skimage.io.imsave(os.path.join(image_dirs["filtros_frequencia"], "camera_original.png"), images_to_load["camera.png"])
print(f"Imagens para Filtros de Frequência salvas em {image_dirs['filtros_frequencia']}")

# Segmentação Watershed - usaremos coins e chelsea
skimage.io.imsave(os.path.join(image_dirs["segmentacao_watershed"], "coins_original.png"), images_to_load["coins.png"])
skimage.io.imsave(os.path.join(image_dirs["segmentacao_watershed"], "chelsea_original.png"), images_to_load["chelsea.png"])
print(f"Imagens para Segmentação Watershed salvas em {image_dirs['segmentacao_watershed']}")

# Crescimento de Regiões - usaremos text e astronaut
skimage.io.imsave(os.path.join(image_dirs["crescimento_regioes"], "text_original.png"), images_to_load["text.png"])
skimage.io.imsave(os.path.join(image_dirs["crescimento_regioes"], "astronaut_original.png"), images_to_load["astronaut.png"])
# Salvar também a imagem 'horse' que é binária e pode ser interessante
skimage.io.imsave(os.path.join(image_dirs["crescimento_regioes"], "horse_original.png"), skimage.img_as_ubyte(images_to_load["horse.png"]))
print(f"Imagens para Crescimento de Regiões salvas em {image_dirs['crescimento_regioes']}")

print("Download e organização de imagens de exemplo concluídos.")

