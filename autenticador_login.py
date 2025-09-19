import cv2, dlib, numpy as np, pickle, os, json, time
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
        email_digitado = input("Digite seu email: ").strip()
        senha_digitada = input("Digite sua senha: ").strip()
        if face_validada and usuario_atual:
            if usuario_atual["email"] == email_digitado and usuario_atual["senha"] == senha_digitada:
                print(f"✔️ Login bem-sucedido! Bem-vindo {usuario_atual['nome']}")
                registrar_log(usuario_atual["email"], True)
                falhas = 0
                validando = False
                break
            else:
                print("❌ Credenciais inválidas! Tente novamente.")
                registrar_log(email_digitado, False)
                falhas += 1
                if falhas >= MAX_FALHAS:
                    print("🚫 Muitas falhas seguidas. Programa bloqueado.")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

cap = cv2.VideoCapture(0)
validando = False
falhas = 0
mensagem_status = ""
validando_anim = 0
estado_tela = ""
usuario_atual = None
face_validada = False

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
                        print("😃 Sorriso detectado! Iniciando validacao...")
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
                    print("❌ Rosto não identificado. Pressione [L] para tentar novamente.")
                    mensagem_status = "nao_identificado"
                    registrar_log("Rosto desconhecido", False)
                    falhas += 1
                    validando = False

            if falhas >= MAX_FALHAS:
                print("🚫 Muitas falhas seguidas. Programa bloqueado.")
                cap.release()
                cv2.destroyAllWindows()
                exit()

    cv2.imshow("Faces", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('l') and not validando:
        validando = True
        estado_tela = ""
        mensagem_status = ""
        face_validada = False
        print("Iniciando tentativa de login. Posicione seu rosto e sorria.")
    elif k == ord('c') and len(rects) == 1:
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()
        if nome and email and senha:
            if email_existe(email):
                print("❌ Já existe um usuário cadastrado com esse e-mail.")
            else:
                db[email] = vec
                pickle.dump(db, open(DB_FILE, "wb"))
                usuarios.append({"nome": nome, "email": email, "senha": senha})
                salvar_usuarios()
                print("✅ Usuário cadastrado:", nome)
