from PIL import Image, ImageDraw, ImageFont

def getListOfLines(text, size):
    numOfParts = len(text)//size
    finalText = []
    start = 0
    for i in range(numOfParts):
        ending = range(start+size, start+size//2, -1)
        for letter in ending:
            try:
                if text[letter] == " ":
                    finalText.append(str(text[start:letter]))
                    text = text[letter:]
            except IndexError:
                break
    if text!='':
      finalText.append(text)
    return finalText    

def applyTextToImage(filename, text):
    try:
        image = Image.open(filename) 
        draw = ImageDraw.Draw(image)
    except FileNotFoundError:
        print("Не найдено изображение")
        return(1)
    width = image.width
    height = image.height
    memeText = getListOfLines(text, 20)    
    h = height//100
    w = width//2
    bottom = 0
    for part in memeText:
        fontsize = width/12
        if memeText.index(part) >= len(memeText)//2:
            bottom += 1
        if bottom == 1:
            h += height - (fontsize*len(memeText)) - 10
        pos = (w, h)
        try:
            font = ImageFont.truetype("./fonts/Impact.ttf", fontsize)
        except IOError:
            font = ImageFont.load_default()
        position = pos
        draw.text(position, part, font=font, fill=(255, 255, 255), anchor = "mt",  stroke_width=2, stroke_fill='black')
        h += fontsize
    filename = filename.split('/')[2]
    image.save(f"Image/Output/{filename}_final.jpg")
    return f"Image/Output/{filename}_final.jpg"