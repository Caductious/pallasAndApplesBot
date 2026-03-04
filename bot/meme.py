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

def putTextOnImage(memeText, draw, w, h, fontsize, font):
    for part in memeText:
        position = (w, h)
        draw.text(position, part, font=font, fill=(255, 255, 255), anchor = "mt",  stroke_width=fontsize/20, stroke_fill='black')
        h += fontsize
    return h

def applyTextToImage(filename, text):
    try:
        image = Image.open(filename) 
        draw = ImageDraw.Draw(image)
    except FileNotFoundError:
        print("Не найдено изображение")
        return(1)
    width = image.width
    height = image.height

    h = height//100
    w = width//2
    if height > width:
        fontsize = height/len(text)*2
    else:
        fontsize = width/len(text)*5

    try:
        font = ImageFont.truetype("./fonts/Impact.ttf", fontsize)
    except IOError:
        font = ImageFont.load_default()

    if "\n" in text:
        text = text.split("\n")
        memeTextList=[[],[]]
        memeTextList[0] =  getListOfLines(text[0], int(width*2/fontsize))
        memeTextList[1] =  getListOfLines(text[1], int(width*2/fontsize))
        print(memeTextList)

        h = putTextOnImage(memeTextList[0], draw, w, h, fontsize, font)

        h += height - (fontsize*(max(len(memeTextList[1]), len(memeTextList[0])))) - fontsize
        memeText = memeTextList[1]
        putTextOnImage(memeTextList[1], draw, w, h, fontsize, font)

    else:
        memeText = getListOfLines(text, int(width*2/fontsize))    
        bottom = 0
        for part in memeText:
            if memeText.index(part) >= len(memeText)//2:
                bottom += 1
            if bottom == 1:
                h += height - (fontsize*len(memeText)) - fontsize
            pos = (w, h)
            position = pos
            draw.text(position, part, font=font, fill=(255, 255, 255), anchor = "mt",  stroke_width=fontsize/20, stroke_fill='black')
            h += fontsize
    filename = filename.split('/')[2]
    image.save(f"Image/Output/{filename}_final.jpg")
    return f"Image/Output/{filename}_final.jpg"
