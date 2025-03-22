from collections import defaultdict, deque
import heapq
from multiprocessing import heap
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
       
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = {baslangic}        
        
        if baslangic == hedef: # eğer başladığımız konum hedef konumumuzla aynı ise 
            return [baslangic] # bu konumu return et 
        
        while kuyruk: # kuyruk boş olmadığı sürece; 
            
            istasyon, rota = kuyruk.popleft() # kuyruk --> (istasyon, rota),   rota --> (istasyon1, istasyon2, ...)
            if istasyon == hedef:
                return rota
            
            for komsu, sure in istasyon.komsular: # istasyonun komşularını kontrol edeceğiz.  komsular --> (istasyon, süre)
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu) # ziyaret edilmediyse ziyaret ediyoruz.
                    yeni_rota = rota + [komsu]  # rotayı gittiğimiz komşu ile güncelliyoruz
                    kuyruk.append((komsu, yeni_rota)) # kuyruğa ekliyoruz 
                    
        return None
        
        

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        İpuçları:
        - heapq modülünü kullanarak bir öncelik kuyruğu oluşturun, HINT: pq = [(0, id(baslangic), baslangic, [baslangic])]
        - Ziyaret edilen istasyonları takip edin
        - Her adımda toplam süreyi hesaplayın
        - En düşük süreye sahip rotayı seçin
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        if baslangic == hedef: # eğer başladığımız konum hedef konumumuzla aynı ise 
            return ([baslangic], 0) # süremiz doğal olarak 0 olmuş oluyor 
        
        pq = [(0, id(baslangic), baslangic, [baslangic])]
        
       
        ziyaret_edildi = set()
        en_kisa_sure = {baslangic.idx: 0}
        
        while pq: # öncelikli kuyruk boş olmadığı sürece;
            
            # pq --> (ağırlık(süre), id(başlangıç), başlangıç, rota)
            toplam_sure, ist_id, istasyon, rota = heapq.heappop(pq)
            
            if istasyon == hedef: # eğer başladığımız konum hedef koumumuzla aynı ise 
                return (rota, toplam_sure) # bu konumu return et 
            
            if istasyon not in ziyaret_edildi: # ziyaret edilmemiş ise ziyaret et
                ziyaret_edildi.add(istasyon)
                
            for komsu, sure in istasyon.komsular: # istasyonun komşularını kontrol edeceğiz
                if komsu not in ziyaret_edildi: # ziyaret edilmediyse
                    yeni_sure = toplam_sure + sure # süreyi güncelle  (f(n) = g(n) + h(n))
                    
                    # eğer bu istasyona daha kısa süre ile ulaşılmadıysa;
                    if not (komsu.idx in en_kisa_sure and yeni_sure >= en_kisa_sure[komsu.idx]):   
                        en_kisa_sure[komsu.idx] = yeni_sure # süreyi güncelliyoruz
                        yeni_rota = rota + [komsu] # rotayı ulaştığımız konum ile güncelliyoruz
                        
                    # öncelikli kuyruğa ekliyoruz 
                    heapq.heappush(pq, (yeni_sure, id(komsu), komsu, yeni_rota))    
        return None


if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Yeşil Hat
    metro.istasyon_ekle("Y1", "Osmangazi", "Yeşil Hat")
    metro.istasyon_ekle("Y2", "Heykel", "Yeşil Hat")
    metro.istasyon_ekle("Y3", "T1", "Yeşil Hat")
    metro.istasyon_ekle("Y4", "Mudanya", "Yeşil Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "Bursa Otogarı", "Mavi Hat")
    metro.istasyon_ekle("M2", "Emek", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Mudanya", "Mavi Hat")
    metro.istasyon_ekle("M4", "Zafer Plaza", "Mavi Hat")
    
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Nilüfer", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Bursa Şehir Hastanesi", "Kırmızı Hat")  # Aktarma noktası
    metro.istasyon_ekle("K3", "Kükürtlü", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "Çekirge", "Kırmızı Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Karacabey", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Mustafakemalpaşa", "Turuncu Hat")
    metro.istasyon_ekle("T3", "Osmangazi", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Güvenevler", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Yeşil Hat bağlantıları
    metro.baglanti_ekle("Y1", "Y2", 5)  # Osmangazi -> Heykel
    metro.baglanti_ekle("Y2", "Y3", 7)  # Heykel -> T1
    metro.baglanti_ekle("Y3", "Y4", 10)  # T1 -> Mudanya
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 4)  # Bursa Otogarı -> Emek
    metro.baglanti_ekle("M2", "M3", 6)  # Emek -> Mudanya
    metro.baglanti_ekle("M3", "M4", 5)  # Mudanya -> Zafer Plaza
    
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 6)  # Nilüfer -> Bursa Şehir Hastanesi
    metro.baglanti_ekle("K2", "K3", 5)  # Bursa Şehir Hastanesi -> Kükürtlü
    metro.baglanti_ekle("K3", "K4", 4)  # Kükürtlü -> Çekirge
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 12)  # Karacabey -> Mustafakemalpaşa
    metro.baglanti_ekle("T2", "T3", 7)  # Mustafakemalpaşa -> Osmangazi
    metro.baglanti_ekle("T3", "T4", 6)  # Osmangazi -> Güvenevler
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("Y2", "M2", 3)  # Heykel aktarma
    metro.baglanti_ekle("K2", "T3", 4)  # Bursa Şehir Hastanesi aktarma
    metro.baglanti_ekle("M4", "T4", 2)  # Zafer Plaza aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: Bursa Otogarı'ndan Zafer Plaza'ya
    print("\n1. Bursa Otogarı'dan Zafer Plaza'ya:")
    rota = metro.en_az_aktarma_bul("M1", "M4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "M4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Nilüfer'den Çekirge'ye
    print("\n2. Nilüfer'den Çekirge'ye:")
    rota = metro.en_az_aktarma_bul("K1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("K1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Osmangazi'den Mudanya'ya
    print("\n3. Osmangazi'den Mudanya'ya:")
    rota = metro.en_az_aktarma_bul("T3", "Y4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T3", "Y4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
