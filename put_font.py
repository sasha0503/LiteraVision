import os
import json

from PIL import Image, ImageDraw, ImageFont

font_path = "/home/oleksandr/Downloads/KyivType/KyivType2020-14-12/KyivType-NoVariable/TTF/KyivTypeSans-Heavy.ttf"
font_size = 60
font_color = (255, 255, 255)
background_color = (0, 0, 0, 128)
background_color_with_opacity = (*background_color[:-1], int(0.2 * 255))
font = ImageFont.truetype(font_path, font_size)


def create_slides(img_path, segment_text, out_folder):
    with open('transcription.json') as f:
        transcription = json.load(f)
        transcription = transcription['word_segments']
        transcription_words = [word['word'] for word in transcription]
        transcription_words = [
            transcription_word.replace('.', '').replace('?', '').replace('!', '').replace(',', '').lower() for
            transcription_word in transcription_words]

    os.makedirs(out_folder, exist_ok=True)
    text_lines = segment_text.split('\n')
    time_config = {}
    last_words_global = []

    for i, text_i in enumerate(text_lines):
        text_y = 50
        text_x = 50
        image = Image.open(img_path)
        draw = ImageDraw.Draw(image)
        words = text_i.split(' ')
        words_cat = []
        for word in words:
            if len(words_cat) and len(words_cat[-1]) < 7 and all(
                    sign not in words_cat[-1] for sign in ['.', '!', '?', ':', ',']):
                words_cat[-1] += ' ' + word
            else:
                words_cat.append(word)
        last_words = [words.split(" ")[-1] for words in words_cat]
        last_words = [last_word.replace('.', '').replace('?', '').replace('!', '').replace(',', '').lower()
                      for last_word in last_words]
        last_words_global.append(last_words)

        for j, word in enumerate(words_cat):
            text_size = draw.textsize(word, font=font)
            text_size = (text_size[0], 65)
            text_y += text_size[1] + 20
            draw.rectangle([text_x, text_y, text_x + text_size[0], text_y + text_size[1]],
                           fill=background_color_with_opacity)
            draw.text((text_x, text_y), word, font=font, fill=font_color)
            image.save(f"{out_folder}/output_image_{i}_{j}.jpg")

    for i, (last_words) in enumerate(last_words_global):
        time_config[i] = []
        for j, word in enumerate(last_words):
            try:
                index = transcription_words.index(word)
                for id in range(index):
                    transcription_words[id] = None
                end = transcription[index]['end']
            except Exception as e:
                print(e)
                end = None
            time_config[i].append(end)
    with open(os.path.join(out_folder, 'time_config.json'), 'w') as f:
        json.dump(time_config, f)


if __name__ == '__main__':
    texts = '''Ви знаєте, як липа шелестить у місячні весняні ночі?
Кохана спить, кохана спить, Піди збуди, цілуй їй очі. Кохана спить…
Ви чули ж бо: так липа шелестить.
Ви знаєте, як сплять старі гаї? Вони все бачать крізь тумани.
Ось місяць, зорі, солов'ї "Я твій" — десь чують дідугани 
А солов'ї! Та ви вже знаєте, як сплять гаї!'''.split('\n')
    images = [os.path.join('images', img) for img in os.listdir('images')]
    images.sort()

    for img_i, (text, img) in enumerate(zip(texts, images)):
        create_slides(img, text, f'output_folder_{img_i}')
