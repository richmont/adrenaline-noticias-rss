from bs4 import BeautifulSoup
import re
from ScraperNoticias.Scraper import Scraper, logger_scraper
from NoticiaAdrenaline import NoticiaAdrenaline

class ScraperAdrenaline(Scraper):
    def __init__(self, url):
        super().__init__(url)
    
    def parse_pagina_lista_noticias(self) -> list:

        def extrair_url_imagem(soup_tag_a):
            elemento_figure = soup_tag_a.find("figure", class_="feed-image")
            elemento_img = elemento_figure.find("img")
            imagem_url_bruta = elemento_img["data-lazy-src"]
            # aplica regex para remover o endereço do processador de imagens do site original
            regex_url_imagem_adrenaline = r"uploads\.adrenaline\.com\.br(.*?)\.jpg" # começa com upload e termina com jpg
            filtro_regex_url_imagem = re.search(regex_url_imagem_adrenaline, imagem_url_bruta)
            if filtro_regex_url_imagem:
                return f"https://{filtro_regex_url_imagem.group(0)}"
            else:
                logger_scraper.warning("URL de imagem da notícia incompatível, retornando logo padrão")
                return "https://www.adrenaline.com.br/wp-content/themes/seox-publishers-child//assets/images/header/logo_adrenaline.svg"

        # converte o html bruto para elemento soup, do bs4
        soup =  BeautifulSoup(self._pagina_completa, "html.parser")
        # elemento container cujos elementos filhos representam uma notícia
        soup_container_lista_noticias = soup.find(
            "div", class_="archive-list-posts"
            )
        # extrai os elementos de notícias para uma lista
        lista_elementos_noticias = soup_container_lista_noticias.find_all("article", {"class":"feed feed-4-list"})
        logger_scraper.debug("Tamanho do elemento container possui %i notícias", len(
            lista_elementos_noticias
            ))
        lista_noticias = []

        for x in lista_elementos_noticias:
            # Maior parte das informações estão na primeira tag "a" do elemento
            primeira_tag_a = x.find("a")
            titulo = primeira_tag_a["title"]
            url = primeira_tag_a["href"]
            url_imagem = extrair_url_imagem(primeira_tag_a)

            elemento_feed_data = x.find("div", class_="feed-data")
            data = elemento_feed_data.find("span").text.strip()

    def parse_conteudo_noticia(self, url_noticia: str) -> NoticiaAdrenaline:
        pass


if __name__ == "__main__":
    url = "https://www.adrenaline.com.br/noticias/"
    scraper = ScraperAdrenaline(url)
    l = scraper.parse_pagina_lista_noticias()