import tkinter as tk
from tkinter import messagebox

class SatrancOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Satranç Oyunu")
        
        self.tahta_boyutu = 8
        self.kare_boyutu = 70
        self.secili_tas = None
        self.secili_konum = None
        self.sira = "beyaz"
        
        # Tahtayı oluştur (8x8 liste)
        self.tahta = self.baslangic_tahtasi()
        
        # Canvas oluştur
        self.canvas = tk.Canvas(
            root, 
            width=self.kare_boyutu * self.tahta_boyutu,
            height=self.kare_boyutu * self.tahta_boyutu
        )
        self.canvas.pack()
        
        # Durum etiketi
        self.durum_label = tk.Label(root, text="Sıra: Beyaz", font=("Arial", 14))
        self.durum_label.pack(pady=10)
        
        # Yeniden başlat butonu
        self.yenile_button = tk.Button(root, text="Yeni Oyun", command=self.yeni_oyun, font=("Arial", 12))
        self.yenile_button.pack(pady=5)
        
        # Mouse tıklama olayı
        self.canvas.bind("<Button-1>", self.tiklama)
        
        self.tahtayi_ciz()
    
    def baslangic_tahtasi(self):
        """Başlangıç tahtasını oluştur"""
        tahta = [[None for _ in range(8)] for _ in range(8)]
        
        # Siyah taşlar
        tahta[0] = ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']
        tahta[1] = ['♟'] * 8
        
        # Beyaz taşlar
        tahta[6] = ['♙'] * 8
        tahta[7] = ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        
        return tahta
    
    def tahtayi_ciz(self):
        """Satranç tahtasını ve taşları çiz"""
        self.canvas.delete("all")
        
        # Kareleri çiz
        for satir in range(self.tahta_boyutu):
            for sutun in range(self.tahta_boyutu):
                x1 = sutun * self.kare_boyutu
                y1 = satir * self.kare_boyutu
                x2 = x1 + self.kare_boyutu
                y2 = y1 + self.kare_boyutu
                
                # Kare rengini belirle
                if (satir + sutun) % 2 == 0:
                    renk = "#F0D9B5"
                else:
                    renk = "#B58863"
                
                # Seçili kareyi vurgula
                if self.secili_konum and self.secili_konum == (satir, sutun):
                    renk = "#FFFF00"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=renk, outline="")
                
                # Taşı çiz
                tas = self.tahta[satir][sutun]
                if tas:
                    self.canvas.create_text(
                        x1 + self.kare_boyutu // 2,
                        y1 + self.kare_boyutu // 2,
                        text=tas,
                        font=("Arial", 40),
                        fill="black"
                    )
    
    def tiklama(self, event):
        """Mouse tıklama olayını işle"""
        sutun = event.x // self.kare_boyutu
        satir = event.y // self.kare_boyutu
        
        if satir >= 8 or sutun >= 8:
            return
        
        tas = self.tahta[satir][sutun]
        
        # Eğer taş seçili değilse
        if self.secili_tas is None:
            if tas and self.tas_rengi(tas) == self.sira:
                self.secili_tas = tas
                self.secili_konum = (satir, sutun)
                self.tahtayi_ciz()
        else:
            # Taşı hareket ettir
            eski_satir, eski_sutun = self.secili_konum
            
            # Geçerli hamle kontrolü
            if self.gecerli_hamle_mi(eski_satir, eski_sutun, satir, sutun):
                # Hamleyi yap
                self.tahta[satir][sutun] = self.secili_tas
                self.tahta[eski_satir][eski_sutun] = None
                
                # Sırayı değiştir
                self.sira = "siyah" if self.sira == "beyaz" else "beyaz"
                self.durum_label.config(text=f"Sıra: {self.sira.capitalize()}")
            
            # Seçimi temizle
            self.secili_tas = None
            self.secili_konum = None
            self.tahtayi_ciz()
    
    def tas_rengi(self, tas):
        """Taşın rengini belirle"""
        beyaz_taslar = ['♙', '♖', '♘', '♗', '♕', '♔']
        return "beyaz" if tas in beyaz_taslar else "siyah"
    
    def gecerli_hamle_mi(self, eski_satir, eski_sutun, yeni_satir, yeni_sutun):
        """Basit hamle kontrolü"""
        tas = self.tahta[eski_satir][eski_sutun]
        hedef = self.tahta[yeni_satir][yeni_sutun]
        
        # Aynı kareye tıklanmış
        if eski_satir == yeni_satir and eski_sutun == yeni_sutun:
            return False
        
        # Kendi taşına hamle yapılamaz
        if hedef and self.tas_rengi(hedef) == self.tas_rengi(tas):
            return False
        
        # Piyon hamlesi
        if tas in ['♙', '♟']:
            yon = -1 if tas == '♙' else 1
            baslangic_satiri = 6 if tas == '♙' else 1
            
            # İleri hamle
            if eski_sutun == yeni_sutun and hedef is None:
                if yeni_satir == eski_satir + yon:
                    return True
                if eski_satir == baslangic_satiri and yeni_satir == eski_satir + 2 * yon:
                    return self.tahta[eski_satir + yon][eski_sutun] is None
            
            # Çapraz yeme
            if abs(eski_sutun - yeni_sutun) == 1 and yeni_satir == eski_satir + yon:
                if hedef and self.tas_rengi(hedef) != self.tas_rengi(tas):
                    return True
            
            return False
        
        # Kale hamlesi
        if tas in ['♖', '♜']:
            if eski_satir == yeni_satir or eski_sutun == yeni_sutun:
                return self.yol_acik_mi(eski_satir, eski_sutun, yeni_satir, yeni_sutun)
            return False
        
        # At hamlesi
        if tas in ['♘', '♞']:
            satir_fark = abs(eski_satir - yeni_satir)
            sutun_fark = abs(eski_sutun - yeni_sutun)
            return (satir_fark == 2 and sutun_fark == 1) or (satir_fark == 1 and sutun_fark == 2)
        
        # Fil hamlesi
        if tas in ['♗', '♝']:
            if abs(eski_satir - yeni_satir) == abs(eski_sutun - yeni_sutun):
                return self.yol_acik_mi(eski_satir, eski_sutun, yeni_satir, yeni_sutun)
            return False
        
        # Vezir hamlesi
        if tas in ['♕', '♛']:
            if eski_satir == yeni_satir or eski_sutun == yeni_sutun or \
               abs(eski_satir - yeni_satir) == abs(eski_sutun - yeni_sutun):
                return self.yol_acik_mi(eski_satir, eski_sutun, yeni_satir, yeni_sutun)
            return False
        
        # Şah hamlesi
        if tas in ['♔', '♚']:
            satir_fark = abs(eski_satir - yeni_satir)
            sutun_fark = abs(eski_sutun - yeni_sutun)
            return satir_fark <= 1 and sutun_fark <= 1
        
        return True
    
    def yol_acik_mi(self, eski_satir, eski_sutun, yeni_satir, yeni_sutun):
        """Yolda engel var mı kontrol et"""
        satir_yon = 0 if eski_satir == yeni_satir else (1 if yeni_satir > eski_satir else -1)
        sutun_yon = 0 if eski_sutun == yeni_sutun else (1 if yeni_sutun > eski_sutun else -1)
        
        kontrol_satir = eski_satir + satir_yon
        kontrol_sutun = eski_sutun + sutun_yon
        
        while kontrol_satir != yeni_satir or kontrol_sutun != yeni_sutun:
            if self.tahta[kontrol_satir][kontrol_sutun] is not None:
                return False
            kontrol_satir += satir_yon
            kontrol_sutun += sutun_yon
        
        return True
    
    def yeni_oyun(self):
        """Oyunu yeniden başlat"""
        self.tahta = self.baslangic_tahtasi()
        self.secili_tas = None
        self.secili_konum = None
        self.sira = "beyaz"
        self.durum_label.config(text="Sıra: Beyaz")
        self.tahtayi_ciz()

# Ana pencereyi oluştur ve oyunu başlat
if __name__ == "__main__":
    root = tk.Root()
    oyun = SatrancOyunu(root)
    root.mainloop()