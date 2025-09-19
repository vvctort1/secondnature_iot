# Autenticação Facial com Dlib, OpenCV + HaarCascades

## Objetivo

Nosso objetivo é implementar um sistema de autenticação em duas etapas adicionando além das credenciais de email e senha, o reconhecimento facial para garantir maior segurança no acesso de usuários. O sistema busca combinar a biometria facial com a validação de login e senha, permitindo ao usuário entrar com suas credenciais somente depois que seu rosto foi validado. Reduzindo riscos de fraude e aumentando a segurança da aplicação.
  <br><br>
## Execução

1. Ao iniciar, o sistema disponibiliza 3 opções ao usuário:
   - "c" para cadastrar um novo usuário;
   - "l" para efetuar um login (onde inicia a validação)
   - "q" para encerrar o programa
  <br><br>
2. Ao utilizar o comando "c", o sistema armazena o rosto do usuário no arquivo db.pkl. E pede ao usuário que escolha endereço de e-mail e senha. Guardando os dados do usuário em um arquivo json;
     <br><br>
4. O comando "l", inicia a validação:
   - No caso do reconhecimento facial falhar, um retângulo vermelho aparece em volta do rosto, e é mostrado no terminal uma mensagem pedindo ao usuário que reinicie a tentativa de validação;
   - Caso o rosto seja reconhecido, um retângulo verde aparece em volta do rosto, com o e-mail atrelado à face mostrada. Além do reconhecimento facial, o sistema pede ao usuário para que ele sorria (garantindo que não está sendo utilizada uma foto estática na tentativa de burlar a verificação), validando a face + sorriso.
       <br><br>
5. No passo final (após a validação facial), o sistema pede ao usuário que digite as credenciais atreladas ao rosto no terminal. Mostrando uma mensagem de sucesso ou falha.
    <br><br>
  Observação: todas as tentativas de validação são registradas em logs.json.
  <br><br>
### Sobre a Segurança

- O sistema não permite que seja cadastrado mais de 1 endereço de email;
- A cada 3 tentativas mal sucedidas de login ou cadastro, o sistema mostra uma mensagem de bloqueio da aplicação, interrompendo a execução do programa;
- É utilizado o email único para atrelar a face às credenciais. Dessa forma, 2 pessoas com o mesmo nome, não podem acessar o sistema com as credenciais uma da outra.
<br><br>

## Dependências utilizadas

Entre as dependências que necessitam instalação, estão: opencv, dlib e numpy. Podendo ser instaladas com o seguinte comando.

python -m pip install cmake opencv-python dlib-bin numpy

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
