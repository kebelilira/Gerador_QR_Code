import re
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import qrcode.constants

class QRCodeApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QR Code")
        self.root.geometry("500x500")

        self.texto = tk.StringVar()
        self.nome_arquivo = tk.StringVar(value="qrcode.png")
        self.cor_frente = tk.StringVar(value="black")
        self.cor_fundo = tk.StringVar(value="white")
        self.tamanho = tk.IntVar(value=10)
        self.borda = tk.IntVar(value=4)

        self.criar_widgets()
    
    def criar_widgets(self):

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Texto/URL para QRCode:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.entry_texto = ttk.Entry(main_frame, textvariable=self.texto, width=40)
        self.entry_texto.grid(row=0, column=1, columnspan=2, pady=(0, 5), sticky=tk.EW)

        ttk.Label(main_frame, text="Nome do arquivo:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.entry_arquivo = ttk.Entry(main_frame, textvariable=self.nome_arquivo, width=30)
        self.entry_arquivo.grid(row=1, column=1, pady=(0, 5), sticky=tk.W)
        ttk.Button(main_frame, text="Selecionar arquivo...", command=self.escolher_arquivo).grid(row=1, column=2, pady=(0, 5), sticky=tk.E)

        settings_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)

        ttk.Label(settings_frame, text="Cor da frente:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(settings_frame, textvariable=self.cor_frente, width=10).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(settings_frame, text="Cor de fundo:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(settings_frame, textvariable=self.cor_fundo, width=10).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(settings_frame, text="Tamanho:").grid(row=2, column=1, sticky=tk.W)
        ttk.Spinbox(settings_frame, from_=1, to=40, textvariable=self.tamanho, width=5).grid(row=2, column=0, sticky=tk.W)

        ttk.Button(main_frame, text="Gerar QR Code", command=self.gerar_qrcode).grid(row=3, column=0, columnspan=3, pady=(10, 0))

        self.preview_label = ttk.Label(main_frame)
        self.preview_label.grid(row=4, column=0, columnspan=3)

        main_frame.columnconfigure(1, weight=1)
    
    def escolher_arquivo(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("ALL files", "*.*")],
            initialfile=self.nome_arquivo.get()
        )
        if filepath:
            self.nome_arquivo.set(filepath)
    
    def gerar_qrcode(self):
        texto = self.texto.get()
        pattern = re.compile(
        r'^(https?|ftp):\/\/'
        r'(\w+(\-\w+)*\.)+'
        r'[a-z]{2,}'
        r'(\/\s*)?$')
        if not texto:
            messagebox.showerror("Erro", "Por favor, insira uma URL para gerar o QR Code.")
            return
        elif not pattern:
            messagebox.showerror("Erro formato inválido", "Por favor, insira uma URL válida.")
            return
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.tamanho.get(),
                border=self.borda.get(),
            )
            qr.add_data(texto)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.cor_frente.get(), back_color=self.cor_fundo.get())

            filename = self.nome_arquivo.get()
            img.save(filename)

            self.mostrar_preview(img)

            messagebox.showinfo(" Sucesso", f" Seu QR Code foi gerado com sucesso!\n\n Salvo como: {filename}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o QR code:\n {str(e)}")

    def mostrar_preview(self, img):
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()

        
