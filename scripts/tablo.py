import pandas as pd
import tkinter as tk
from tkinter import ttk

# CSV dosyasını yükle
df = pd.read_csv('new_veri.csv')

# İlk 20 satırı seç
df_subset = df[['author', 'comment']].head(20)

# Tkinter penceresini oluştur
root = tk.Tk()

# Pencereyi tam ekran yapıyoruz
root.attributes('-fullscreen', True)  # Tam ekran yap

# Pencere başlığı
root.title("Kullanıcı Yorumları Tablosu")

# Treeview widget'ını oluştur
tree = ttk.Treeview(root)

# Sütunları tanımla
tree['columns'] = ('author', 'comment')

# Sütun başlıklarını ayarla
tree.heading('#0', text='', anchor='w')
tree.heading('author', text='Kullanıcı Adı - Yorum', anchor='w')
tree.heading('comment', text='', anchor='w')

# Sütunların genişliklerini ayarla
tree.column('#0', width=0, stretch=tk.NO)
tree.column('author', anchor='w', width=1000)  # Kullanıcı adı ve yorum için genişlik
tree.column('comment', anchor='w', width=800)

# Veriyi tabloya ekle
for index, row in df_subset.iterrows():
    # Kullanıcı adı ve yorumları 'Kullanıcı Adı - Yorum' formatında ekleyelim
    item_id = tree.insert('', 'end', values=(f"{row['author']} - {row['comment']}", ''))
    
    # Satır numarasına göre çizgi ekle
    if index % 2 == 0:
        tree.item(item_id, tags=('even',))
    else:
        tree.item(item_id, tags=('odd',))

# Satırlar arasına çizgiler ekleyelim
tree.tag_configure('even', background='#f0f0f0')  # Çift satırlar için arka plan rengi
tree.tag_configure('odd', background='#ffffff')  # Tek satırlar için arka plan rengi

# Treeview widget'ını pencereye ekle
tree.pack(fill="both", expand=True)

# Pencereyi sürekli açık tut
root.mainloop()
