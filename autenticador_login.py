import cv2, dlib, numpy as np, pickle, os, json, sys, time
from datetime import datetime
import threading

PREDICTOR = "shape_predictor_5_face_landmarks.dat"
RECOG = "dlib_face_recognition_resnet_model_v1.dat"
DB_FILE = "db.pkl"
USERS_FILE = "usuarios.json"
LOG_FILE = "logs.json"
THRESH = 0.6
MAX_FALHAS = 3

db = pickle.load(open(DB_FILE, "rb")) if os.path.exists(DB_FILE) else {}
usuarios = json.load(open(USERS_FILE, "r", encoding="utf-8")) if os.path.exists(USERS_FILE) else []

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(PREDICTOR)
rec = dlib.face_recognition_model_v1(RECOG)
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
 
#------------------------------------------------------------------

def salvar_usuarios():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def registrar_log(usuario, sucesso):
    log = {
        "email": usuario,
        "horario": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "sucesso" if sucesso else "falha"
    }
    data = json.load(open(LOG_FILE, "r", encoding="utf-8")) if os.path.exists(LOG_FILE) else []
    data.append(log)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def email_existe(email):
    for u in usuarios:
        if u["email"] == email:
            return True
    return False

def buscar_usuario_por_email(email):
    for u in usuarios:
        if u["email"] == email:
            return u
    return None

def input_credenciais():
    global falhas, usuario_atual, validando, face_validada
    while True:
        limpar_terminal()
        print("CREDENCIAIS")
        email_digitado = input("Email: ").strip()
        senha_digitada = input("Senha: ").strip()
        if face_validada and usuario_atual:
            if usuario_atual["email"] == email_digitado and usuario_atual["senha"] == senha_digitada:
                print("\n✔️ Login bem-sucedido! Entrando...")
                registrar_log(usuario_atual["email"], True)
                falhas = 0
                validando = False
                time.sleep(3)
                limpar_terminal()
                print(f"Bem-vindo {usuario_atual['nome']}!")
                time.sleep(5)
                print("Logout...")
                time.sleep(3)
                limpar_terminal()
                print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")
                break
            elif (usuario_atual["email"] != email_digitado or usuario_atual["senha"] != senha_digitada):
                falhas += 1
                if falhas < MAX_FALHAS:
                    print("\n❌ Credenciais inválidas! Tente novamente.")
                    time.sleep(2)
                else:
                    break
                
                registrar_log(email_digitado, False)

def limpar_terminal():
    """Limpa o terminal do console."""
    if sys.platform.startswith('win'):
        os.system('cls')  
    else:
        os.system('clear') 
 # ----------------------------------------------------------------------       

cap = cv2.VideoCapture(0)
validando = False
falhas = 0
mensagem_status = ""
validando_anim = 0
estado_tela = ""
usuario_atual = None
face_validada = False

limpar_terminal()
print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")

while True:
    ok, frame = cap.read()
    if not ok: break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(rgb, 0)

    if len(rects) == 0 and not validando:
        mensagem_status = ""

    for r in rects:
        shape = sp(rgb, r)
        chip = dlib.get_face_chip(rgb, shape)
        vec = np.array(rec.compute_face_descriptor(chip), dtype=np.float32)

        if validando and db:
            email_reconhecido, dist = None, 999
            for e, v in db.items():
                d = np.linalg.norm(vec - v)
                if d < dist:
                    email_reconhecido, dist = e, d

            if dist < THRESH:
                cor = (0,255,0)
                cv2.rectangle(frame, (r.left(), r.top()), (r.right(), r.bottom()), cor, 2)
                cv2.putText(frame, email_reconhecido, (r.left(), r.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)

                face_roi = gray[r.top():r.bottom(), r.left():r.right()]
                smiles = smile_cascade.detectMultiScale(face_roi, scaleFactor=1.8, minNeighbors=20)

                if len(smiles) == 0 and estado_tela == "":
                    if mensagem_status != "sorria":
                        usuario_atual = buscar_usuario_por_email(email_reconhecido)
                        if usuario_atual:
                            print(f"\nRosto reconhecido: {usuario_atual['nome']}. Por favor, sorria para continuar.")
                        mensagem_status = "sorria"
                    cv2.putText(frame, "Sorria :)", (r.left(), r.bottom()+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

                elif len(smiles) > 0 and estado_tela == "":
                    if mensagem_status != "validando":
                        print("\n😃 Sorriso detectado! Iniciando validacao. Continue sorrindo.")
                        mensagem_status = "validando"
                        validando_anim = 30
                    if validando_anim > 0:
                        texto = "Validando" + "." * ((30 - validando_anim)//10 + 1)
                        cv2.putText(frame, texto, (r.left(), r.bottom()+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
                        validando_anim -= 1
                    else:
                        estado_tela = "credenciais"
                        face_validada = True
                        t = threading.Thread(target=input_credenciais)
                        t.start()

                elif estado_tela == "credenciais":
                    cv2.putText(frame, "Digite suas credenciais", (r.left(), r.bottom()+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            else:
                cor = (0,0,255)
                cv2.rectangle(frame, (r.left(), r.top()), (r.right(), r.bottom()), cor, 2)
                cv2.putText(frame, "Rosto nao identificado", (r.left(), r.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)
                if mensagem_status != "nao_identificado":
                    print("\n❌ Rosto não identificado. Pressione [L] para tentar novamente.")
                    mensagem_status = "nao_identificado"
                    registrar_log("Rosto desconhecido", False)
                    falhas += 1
                    validando = False

            if falhas >= MAX_FALHAS:
                print("\n🚫 Muitas falhas seguidas. Programa bloqueado.")
                time.sleep(4)
                cap.release()
                cv2.destroyAllWindows()
                exit()
                
        elif validando and not db:
            cor = (0,0,255)
            cv2.rectangle(frame, (r.left(), r.top()), (r.right(), r.bottom()), cor, 2)
            cv2.putText(frame, "Rosto nao identificado", (r.left(), r.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)
            registrar_log("Rosto desconhecido", False)
            print("\nRosto não identificado! Voltando ao menu...")
            falhas += 1
            time.sleep(3)
            validando = False
            limpar_terminal()
            print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")
            
    cv2.imshow("Faces", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('l') and not validando:
        validando = True
        estado_tela = ""
        mensagem_status = ""
        face_validada = False
        limpar_terminal()
        print("Iniciando tentativa de login. Posicione seu rosto e sorria.")
    elif k == ord('c') and len(rects) == 0:
        print("\nProcurando rosto...")
    elif k == ord('c') and len(rects) == 1:  
        limpar_terminal()
        print("⚠️ Aviso de Privacidade\n")
        print("Ao prosseguir com o cadastro, você concorda que sua imagem facial será coletada e armazenada em nosso sistema exclusivamente para fins de autenticação.\n")
        prosseguir = input("S/N: ").lower().strip()
        
        if prosseguir == "s":
            
            limpar_terminal()
            print("CADASTRO\n")
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            senha = input("Senha: ").strip()
            
            if nome and email and senha:
                if email_existe(email):
                    print("\n❌ Já existe um usuário cadastrado com esse e-mail. Voltando ao menu...")
                    time.sleep(3)
                    limpar_terminal()
                    print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")
                else:
                    db[email] = vec
                    pickle.dump(db, open(DB_FILE, "wb"))
                    usuarios.append({"nome": nome, "email": email, "senha": senha})
                    salvar_usuarios()
                    print("✅ Cadastro realizado! Voltando ao menu...")
                    time.sleep(3)
                    limpar_terminal()
                    print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")
        elif prosseguir == "n":
            print("\nVoltando ao menu...")
            time.sleep(3)
            limpar_terminal()
            print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")
            continue
        else:
            print("\nCaractere não reconhecido.")
            time.sleep(3)
            limpar_terminal()
            print("[c]=Cadastrar  [l]=Realizar Login  [q]=Sair")
            
        
