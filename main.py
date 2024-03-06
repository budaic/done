from PIL import Image
import pytesseract
import json

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

class Betu:
    def __init__(self, box):
        if len(box)<6:
            self.char = '!'
            self.felso = -1
            self.also = -1
            self.bal = -1
            self.jobb = -1
        else:
            self.char = box[0]
            self.felso = int(box[4])
            self.also = int(box[2])
            self.bal = int(box[1])
            self.jobb = int(box[3])

    def __lt__(self, other):
        return self.bal<other.bal

def betulista_to_string(betulista):
    return str(''.join([i.char for i in betulista]))

class Sor:
    def __init__(self, uj:Betu):
        self.felso=uj.felso
        self.also=uj.also
        self.lista = ""
        self.lista+=uj.char
        self.betuk = [uj]
        self.lukid = 0
        self.dxmax = 0
        self.betumeret = uj.jobb-uj.bal
        self.luk_meret_min = self.betumeret*5

    def benne_van_e(self, uj):
        '''
        if uj.felso<=self.felso and uj.felso>=self.also:
            return True
        if uj.also<=self.felso and uj.also>=self.also:
            return True
        if uj.felso>=self.felso and uj.also<=self.also:
            return True
        '''

        if (uj.felso>=self.also and uj.felso<=self.felso) or (uj.also>=self.also and uj.also<=self.felso) or (self.felso>=uj.also and self.felso<=uj.felso):
            return True
        return False
    
    def hozzaad(self, uj):
        self.also = min(self.also, uj.also)
        self.felso = max(self.felso, uj.felso)
        self.lista+=uj.char
        self.betuk.append(uj)



def image_kezelo(image_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Use pytesseract to convert the image to text, specifying Hungarian language
    boxes = pytesseract.image_to_boxes(img, lang='eng')
    betuk=[Betu(i.split(' ')) for i in boxes.split('\n')]
    

    sorlista = [Sor(betuk[0])]

    for b in betuk[1:]:
        sikerult_e = False
        for sorid in range(len(sorlista)):
            if sorlista[sorid].benne_van_e(b) and not sikerult_e:
                #print(f"{sorlista[sorid].lista} + {b.char}, ({sorlista[sorid].felso}, {sorlista[sorid].also}), ({b.felso}, {b.also})")
                #i = input()
                sorlista[sorid].hozzaad(b)
                sikerult_e = True
                break
        if not sikerult_e:
            '''
            print(f"Uj sor: {b.char}, ({b.felso}, {b.also})")
            i = input()
            if i=='d':
                for sorid in range(len(sorlista)):
                    print(f"{sorlista[sorid].benne_van_e(b)}: ({sorlista[sorid].felso}, {sorlista[sorid].also}), ({b.felso}, {b.also})")
            '''

            sorlista.append(Sor(b))

    # print(len(sorlista))

    # Sorban vannak
    for sorid in range(len(sorlista)):
        sorlista[sorid].betuk.sort()

    output_lista = []

    for sorid in range(len(sorlista)):
        for betuid in range(len(sorlista[sorid].betuk)-1):
            if sorlista[sorid].betuk[betuid+1].bal-sorlista[sorid].betuk[betuid].bal>sorlista[sorid].luk_meret_min:
                sorlista[sorid].lukid = betuid+1
                sorlista[sorid].dxmax = sorlista[sorid].betuk[betuid+1].bal-sorlista[sorid].betuk[betuid].bal
        # print(betulista_to_string(sorlista[sorid].betuk[:sorlista[sorid].lukid])+"       "+betulista_to_string(sorlista[sorid].betuk[sorlista[sorid].lukid:]))
        if(not sorlista[sorid].lukid==0):
            app_dict = {'Item_name': betulista_to_string(sorlista[sorid].betuk[:sorlista[sorid].lukid]), 'Item_price': betulista_to_string(sorlista[sorid].betuk[sorlista[sorid].lukid:])}
            output_lista.append(app_dict)

    # JSON betoltes
    with open ('json_test.json', 'w') as f:
        json.dump(output_lista, f, indent=4)
    

# Replace 'path_to_receipt.jpg' with the path to your receipt image
if __name__ == '__main__':
    receipt_image_path = 'test_receipt.png'
    image_kezelo(receipt_image_path)

