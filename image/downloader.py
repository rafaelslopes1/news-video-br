from news.content import NewsContent
import requests
import shutil


class ImageDownloader:
    def download_all_images(self, content: NewsContent):
        downloaded_images = []

        for sentence_index in range(len(content.sentences)):
            image_urls = content.sentences[sentence_index]["images"]

            for image_index in range(len(image_urls)):
                image_url = image_urls[image_index]
                file_name = f"{sentence_index}-original.png"
                try:
                    if image_url in downloaded_images:
                        raise Exception("Imagem já foi baixada")

                    self.__download_image(image_url, file_name)
                    print(
                        f"> [{sentence_index}][{image_index}] Baixou imagem com sucesso: {image_url}")

                    downloaded_images.append(image_url)

                    break
                except Exception:
                    print(f"> [{sentence_index}][{image_index}] Erro ao baixar {image_url}")

        return downloaded_images

    def __download_image(self, image_url: str, file_name: str):
        res = requests.get(image_url, stream=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
        else:
            raise Exception("Erro na requisição da imagem")
