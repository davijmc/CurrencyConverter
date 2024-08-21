import customtkinter
import requests

# Configurar o modo de aparência
customtkinter.set_appearance_mode("dark")

# Criar a janela principal
root = customtkinter.CTk()
root.title("Interface Gráfica")
root.geometry("768x372")  # Configurar o tamanho inicial da janela

# Frame para alinhar elementos à esquerda, ajustando o tamanho
left_frame = customtkinter.CTkFrame(root, width=300)
left_frame.pack(side="left", padx=20, pady=20, fill="y", expand=False)

# Definir uma fonte maior para os textos
font_large = customtkinter.CTkFont(size=16)  # Tamanho da fonte 16

# Caixa de entrada para valores em reais
entry_label = customtkinter.CTkLabel(left_frame, text="Digite o valor a ser convertido:", font=font_large)
entry_label.pack(anchor="center", pady=10)
entry = customtkinter.CTkEntry(left_frame, font=font_large)
entry.pack(anchor="center", pady=10)

# Primeira combo box com três opções
combo1_label = customtkinter.CTkLabel(left_frame, text="Moeda inicial:", font=font_large)
combo1_label.pack(anchor="center", pady=10)
combo1 = customtkinter.CTkComboBox(left_frame, values=["BRL", "BTC", "EUR", "USD"], font=font_large)
combo1.pack(anchor="center", pady=10)

# Botão
button = customtkinter.CTkButton(left_frame, text="Converter", font=font_large, command=lambda: on_button_click())
button.pack(anchor="center", pady=20)

# Texto centralizado à direita
right_frame = customtkinter.CTkFrame(root)
right_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

centered_text = customtkinter.CTkLabel(right_frame, text="Valor convertido: ", anchor="center", font=font_large)
centered_text.pack(pady=10)

# Segunda combo box com três opções abaixo do texto centralizado
combo2_label = customtkinter.CTkLabel(right_frame, text="Moeda final:", font=font_large)
combo2_label.pack(anchor="center", pady=10)
combo2 = customtkinter.CTkComboBox(right_frame, values=["BRL", "BTC", "EUR", "USD"], font=font_large)
combo2.pack(anchor="center", pady=10)

# clique do botão
def on_button_click():
    if combo1.get() == combo2.get():
        centered_text.configure(text="Selecione moedas diferentes")
        return
    vdig = "Erro"
    try:
        vdig = float(entry.get())
    except:
        centered_text.configure(text="Digite um valor válido")
    if isinstance(vdig, float):
        #print("Val:", vdig)
        # Gambiarra pra funcionar converção de BRL para BTC
        coin1 = combo1.get()
        coin2 = combo2.get()
        if(coin1 == "BRL") and (coin2 == "BTC"):
            flag = 1
        else:
            flag = 0
        apiResp = getResult()
        #print("API:", apiResp)
        try:
            apiResp = float(apiResp)
        except:
            centered_text.configure(text=apiResp)
        if isinstance(apiResp, float):
            if(flag):
                result = vdig / apiResp
            else:
                result = apiResp * vdig
            centered_text.configure(text="Valor convertido: {:.2f}".format(result))
        else:
            centered_text.configure(text=apiResp)

def getResult():
    coin1 = combo1.get()
    coin2 = combo2.get()
    if(coin1 == "BRL") and (coin2 == "BTC"):
        coin1 = "BTC"
        coin2 = "BRL"
    moeda = f"{coin1}-{coin2}"
    
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    # Fazer a requisição GET para a API
    response = requests.get(url)
    
    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parsear o JSON da resposta
        dados = response.json()
        # Extrair a cotação da moeda
        chave = f"{moeda.replace('-', '')}"
        if chave in dados:
            return dados[chave]['bid']  # Retorna o valor de 'bid' (compra)
        else:
            return "Moeda não encontrada na resposta."
    else:
        return "Erro ao acessar a API."
    
# Iniciar o loop principal
root.mainloop()
