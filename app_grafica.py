import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import time
import threading # Para que la app no se congele
from cryptography.fernet import Fernet

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CipherGuard Pro v2.0")
        self.geometry("500x450")

        # --- Interfaz Visual ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.main_frame, text="🛡️ CipherGuard Pro", font=("Roboto", 26, "bold"))
        self.label.pack(pady=(30, 10))

        self.subtitle = ctk.CTkLabel(self.main_frame, text="Seguridad de nivel bancario", font=("Arial", 12), text_color="gray")
        self.subtitle.pack(pady=(0, 20))

        # Botones
        self.btn_cifrar = ctk.CTkButton(self.main_frame, text="🔒 CIFRAR ARCHIVO", command=self.iniciar_cifrado, 
                                       height=45, font=("Roboto", 14, "bold"), corner_radius=10)
        self.btn_cifrar.pack(pady=10, padx=50, fill="x")

        self.btn_descifrar = ctk.CTkButton(self.main_frame, text="🔓 DESCIFRAR ARCHIVO", command=self.iniciar_descifrado, 
                                          height=45, font=("Roboto", 14, "bold"), corner_radius=10,
                                          fg_color="transparent", border_width=2)
        self.btn_descifrar.pack(pady=10, padx=50, fill="x")

        # Barra de Progreso
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=300)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.status_label = ctk.CTkLabel(self.main_frame, text="Listo para proteger", font=("Arial", 13))
        self.status_label.pack(pady=10)

        # Asegurar llave
        if not os.path.exists("llave.key"):
            with open("llave.key", "wb") as k: k.write(Fernet.generate_key())

    # --- Lógica de Hilos ---
    def iniciar_cifrado(self):
        archivo = filedialog.askopenfilename()
        if archivo:
            # Bloqueamos botones para evitar errores
            self.toggle_botones("disabled")
            # Lanzamos el proceso en un hilo separado
            threading.Thread(target=self.proceso_seguro, args=(archivo, "cifrar")).start()

    def iniciar_descifrado(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos cifrados", "*.enc")])
        if archivo:
            self.toggle_botones("disabled")
            threading.Thread(target=self.proceso_seguro, args=(archivo, "descifrar")).start()

    def proceso_seguro(self, path, modo):
        try:
            self.status_label.configure(text=f"Procesando archivo...", text_color="yellow")
            
            # Simulamos progreso visual
            for i in range(1, 11):
                time.sleep(0.1) # Simula carga
                self.progress_bar.set(i / 10)
            
            with open("llave.key", "rb") as k: key = k.read()
            fernet = Fernet(key)
            
            with open(path, "rb") as f: data = f.read()
            
            if modo == "cifrar":
                resultado = fernet.encrypt(data)
                out = path + ".enc"
                msg = "Cifrado exitoso"
            else:
                resultado = fernet.decrypt(data)
                out = path.replace(".enc", "_recuperado.txt")
                msg = "Descifrado exitoso"

            with open(out, "wb") as f: f.write(resultado)
            
            self.status_label.configure(text=f"✅ {msg}", text_color="#4ade80")
            messagebox.showinfo("Éxito", f"Operación completada:\n{os.path.basename(out)}")
            
        except Exception as e:
            self.status_label.configure(text="❌ Error en el proceso", text_color="#f87171")
            messagebox.showerror("Error", "No se pudo procesar. Verifique la llave o el archivo.")
        
        finally:
            self.toggle_botones("normal")
            self.progress_bar.set(0)

    def toggle_botones(self, estado):
        self.btn_cifrar.configure(state=estado)
        self.btn_descifrar.configure(state=estado)

if __name__ == "__main__":
    app = App()
    app.mainloop()
