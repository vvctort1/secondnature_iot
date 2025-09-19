# Autenticação Facial com Dlib, OpenCV + HaarCascades

## Objetivo
<p align='justify'>
  &nbsp;&nbsp;&nbsp;&nbsp;Nosso objetivo é implementar um sistema de autenticação em duas etapas, adicionando além das credenciais de e-mail e senha, o reconhecimento facial para garantir maior segurança no acesso de usuários.  
O sistema busca combinar a biometria facial com a validação de login e senha, permitindo ao usuário entrar com suas credenciais somente depois que seu rosto foi validado, reduzindo riscos de fraude e aumentando a segurança da aplicação.  
</p>


---

## Execução

1. **Ao iniciar, o sistema disponibiliza 3 opções ao usuário:**
   - `c` → cadastrar um novo usuário  
   - `l` → efetuar um login (inicia a validação)  
   - `q` → encerrar o programa  

2. **Cadastro (`c`):**  
   - O sistema armazena o rosto do usuário no arquivo `db.pkl`;  
   - Pede ao usuário e-mail e senha, salvando-os em `usuarios.json`.  

3. **Login (`l`):**  
   - Se o reconhecimento facial falhar, um **retângulo vermelho** aparece em volta do rosto e o terminal exibe uma mensagem pedindo para reiniciar a validação;  
   - Se o rosto for reconhecido, um **retângulo verde** aparece em volta do rosto com o e-mail associado.  
   - O sistema solicita que o usuário **sorria** para validar que não é uma foto estática.  

4. **Credenciais finais:**  
   - Após a validação facial + sorriso, o usuário digita e-mail e senha;  
   - O sistema informa **sucesso** ou **falha**.  

> Todas as tentativas de validação são registradas em `logs.json`.  

---

### Sobre a Segurança

- Não é permitido cadastrar mais de um usuário com o mesmo e-mail;  
- A cada **3 tentativas mal-sucedidas**, o sistema bloqueia a aplicação;  
- O e-mail único é utilizado como chave para atrelar a face às credenciais.  

---

## Dependências utilizadas

Entre as dependências necessárias: **OpenCV**, **Dlib** e **NumPy**.  

Podem ser instaladas com:  

```bash
python -m pip install cmake opencv-python dlib-bin numpy
```

<br>


## Principais Parâmetros

THRESH → limiar de distância para considerar duas faces iguais. (mais alto: mais falso positivo = menor precisão)

MAX_FALHAS → número máximo de tentativas antes do bloqueio do sistema.
<br><br>
### Arquivos de persistência

db.pkl → embeddings faciais.

usuarios.json → lista de usuários cadastrados.

logs.json → histórico de acessos (sucesso/falha).


## Nota ética e legal

Este sistema manipula dados biométricos (faces), que pela Lei Geral de Proteção de Dados Pessoais (LGPD – Lei 13.709/2018) são classificados como dados sensíveis.
Portanto, sua utilização exige:

- Consentimento explícito do usuário para coleta e armazenamento da imagem/descritor facial.

- Garantia de que os dados são usados apenas para autenticação e não para outros fins.

- Armazenamento seguro dos arquivos (db.pkl, usuarios.json, logs.json), com acesso restrito.

- Possibilidade de exclusão definitiva dos dados do usuário caso solicitado.

⚠️ Importante: este projeto é um protótipo acadêmico/experimental. Para uso em produção, recomenda-se implementar criptografia, anonimização de embeddings e controles adicionais de privacidade.


## Integrantes
<table>
  <tr>
    <th>Nome</th>
    <th>RM</th>
    <th>Turma</th>
  </tr>
  <tr>
    <td>Arthur Baldissera Claumann Marcos</td>
    <td>550219</td>
    <td>3ESPF</td>
  </tr>
  <tr>
    <td>Gabriel Genaro Dalaqua</td>
    <td>551986</td>
    <td>3ESPF</td>
  </tr>
  <tr>
    <td>Paloma Mirela dos Santos Rodrigues</td>
    <td>551321</td>
    <td>3ESPF</td>
  </tr>
  <tr>
    <td>Ricardo Ramos Vergani</td>
    <td>550166</td>
    <td>3ESPF</td>
  </tr>
  <tr>
    <td>Victor Kenzo Toma</td>
    <td>551649</td>
    <td>3ESPF</td>
  </tr>
</table>
