import pyautogui
from pyautogui import ImageNotFoundException
import time as tempo
import pandas as pd
import pyperclip
import sys
from datetime import *

#Leitura da tabela que contém os alunos 
tabela = pd.read_csv('tabelaAlunos.csv', delimiter=';')

#Clico no vs code para acessar o sipac
pyautogui.click(1300, 1056)

#contador que vai auxiliar o acesso aos alunos da tabela
n = 0

alunoPendente = []
documentoPendente = []
alunoAtivo = []
documentoAtivo = []

for i in tabela.itertuples():

    #Pausa de meio segundo entre os comandos 
    pyautogui.PAUSE = 0.5
    
    #Clico em um local qualquer da tela do sipac para selcionar a aba
    pyautogui.click(300, 300)

    #Movo o scroll o máximo para cima
    pyautogui.scroll(+10000)

    #Localizo o espaço onde irei inserir o nome do aluno
    try:
        nomeAluno = pyautogui.locateOnScreen('Imagens de Referência/nomedoaluno.png')
        nomeAluno = pyautogui.center(nomeAluno)
    except:
        ImageNotFoundException()

    #Clico três vezes, colo o nome do aluno no respectivo local
    pyautogui.tripleClick(nomeAluno[0]+200, nomeAluno[1])
    pyperclip.copy(tabela.loc[n, 'Aluno'])
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

    #Localizo o topo da página. Se o programa não localizar, é pq a página atualizou.
    paginaAtualizada = False
    while paginaAtualizada == False:
        try:
            pyautogui.locateOnScreen('Imagens de Referência/topodapagina.png')
        except:
            ImageNotFoundException()
            paginaAtualizada = True

    #Movo o scroll o máximo para cima
    pyautogui.scroll(+10000)
    #Movo o scroll o suficiente para acessar a lupa do documento
    pyautogui.scroll(-500)
    #Clico na lupa
    pyautogui.click(1349, 1001)

    #Localizo a pagina do documento. Se o programa não localizar, ele continua tentando.
    paginaAtualizada = False
    while paginaAtualizada == False:
        try:
            pyautogui.locateOnScreen('Imagens de Referência/documento.png')
            paginaAtualizada = True
        except:
            ImageNotFoundException()

    #Localizo a situaçao do documento
    situacao = pyautogui.locateOnScreen('Imagens de Referência/situacao.png')
    situacao = pyautogui.center(situacao)

    pyautogui.tripleClick(situacao[0]+45, situacao[1])
    pyautogui.hotkey('ctrl', 'c')
    novoEstadoDoc = pyperclip.paste()

    #No caso do documento com pendência com pendência de assinatura
    if novoEstadoDoc == ' PENDENTE DE ASSINATURA ':
        tabela.loc[n, 'Situação'] = 'Pendente de Assinatura'
        tabela.loc[n, 'Enviar Documento'] = 'Não'
        pyautogui.hotkey('alt', 'F4')

        #Array que vai receber o nome do aluno com pendência
        alunoPendente.append(tabela.loc[n, 'Aluno'])

        if tabela.loc[n, 'Tipo de Documento'] == "TCE":
            documentoPendente.append("TCE")
        elif tabela.loc[n, 'Tipo de Documento'] == "TR":
            documentoPendente.append("TR")
        elif tabela.loc[n, 'Tipo de Documento'] == "TA":
            documentoPendente.append("TA")


    #No caso do TCE ativo
    elif novoEstadoDoc == ' ATIVO ':
        tabela.loc[n, 'Situação'] = 'Ativo'
        tabela.loc[n, 'Enviar Documento'] = 'Sim'

        alunoAtivo.append(tabela.loc[n, 'Aluno'])

        if tabela.loc[n, 'Tipo de Documento'] == "TCE":
            documentoAtivo.append("TCE")
        elif tabela.loc[n, 'Tipo de Documento'] == "TR":
            documentoAtivo.append("TR")
        elif tabela.loc[n, 'Tipo de Documento'] == "TA":
            documentoAtivo.append("TA")

        assunto = pyautogui.locateOnScreen('Imagens de Referência/assunto.png')
        assunto = pyautogui.center(assunto)

        pyautogui.tripleClick(assunto[0]+70, assunto[1])
        pyautogui.hotkey('ctrl', 'c')
        nomeArquivo = pyperclip.paste()
        nomeArquivo = nomeArquivo.upper()
        if tabela.loc[n, 'Tipo de Documento'] == "TCE":
            nomeArquivo = nomeArquivo.replace('TERMO', 'TCE')
            nomeArquivo = nomeArquivo + ' ASSINADO'
        elif tabela.loc[n, 'Tipo de Documento'] == "TR":
            nomeArquivo = nomeArquivo.replace('TERMO RESCISAO', 'TR')
            nomeArquivo = nomeArquivo + ' ASSINADO'
        elif tabela.loc[n, 'Tipo de Documento'] == "TA":
            nomeArquivo = nomeArquivo.replace('TERMO ADITIVO', 'TA')
            nomeArquivo = nomeArquivo + ' ASSINADO'
        pyautogui.scroll(-1000000000)
        pyautogui.scroll(-1000000000)
        pyautogui.scroll(-1000000000)

        salvardocumento = pyautogui.locateOnScreen('Imagens de Referência/salvardocumento.png')
        salvardocumento = pyautogui.center(salvardocumento)

        pyautogui.click(salvardocumento)

        paginaAtualizada = False
        while paginaAtualizada == False:
            try:
                baixar = pyautogui.locateOnScreen('Imagens de Referência/baixar.png')
                paginaAtualizada = True
            except:
                ImageNotFoundException()

        pyautogui.click(pyautogui.center(baixar))
        pyperclip.copy(nomeArquivo)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        pyautogui.hotkey('alt', 'F4')
        pyautogui.hotkey('alt', 'F4')

        #PARA ENVIAR PELO EMAIL AUTOMATICO 
        #   |
        #   V

        # pyautogui.PAUSE = 0.8

        # pyautogui.hotkey('ctrl','shift','tab')
        # pyautogui.press('/')
        # pyperclip.copy(tabela.loc[n, 'Aluno'])
        # pyautogui.hotkey('ctrl', 'v')
        # pyautogui.press('enter')
        # tempo.sleep(3)
        # pyautogui.press('x')
        # pyautogui.press('enter')
        # pyautogui.press('r')

        # pyperclip.copy(nomeArquivo)
        # pyautogui.hotkey('win','e')
        # pyautogui.hotkey('ctrl','f')
        # pyautogui.hotkey('ctrl','v')
        # tempo.sleep(1)
        # pyautogui.press('enter')
        # pyautogui.hotkey('ctrl','space')
        # pyautogui.hotkey('ctrl', 'c')
        # pyautogui.hotkey('alt', 'F4')

        # pyautogui.write('Termo assinado.')
        # pyautogui.hotkey('ctrl','v')
        # pyautogui.press('esc')
        # pyautogui.hotkey('ctrl','tab')

        # pyautogui.PAUSE = 0.5

    else:
        break
    tabela.to_csv('tabelaAlunos.csv',  sep=';', index=False)
    n += 1

pyperclip.copy('')

#Automação para inserir a atividade no relatório

atividade = 'Processos - Verificar pendências de assinaturas de TCE, TA ou TR (sigaa > estágio > gerenciar estágios > situação aguardando assinatura)'

pyautogui.hotkey('ctrl','tab')

if len(alunoPendente) != 0:
    for aluno, documento in zip(alunoPendente, documentoPendente):

        pyperclip.copy(atividade)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')
        pyautogui.write('1')
        pyautogui.press('tab')
        pyautogui.write('0:01:0')
        pyautogui.press('tab')
        data = date.today()
        data = str(data)
        data = data.split('-')
        data.reverse()
        data = "/".join(data)
        pyautogui.write(data)
        pyautogui.press('tab')
        obs = "%s %s Pendente de Assinatura" % (documento, aluno)
        pyperclip.copy(obs)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('down')
        pyautogui.press('left')
        pyautogui.press('left')
        pyautogui.press('left')
        pyautogui.press('left')
    
if len(alunoAtivo) != 0:
    for aluno, documento in zip(alunoAtivo, documentoAtivo):
        pyperclip.copy(atividade)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')
        pyautogui.write('1')
        pyautogui.press('tab')
        pyautogui.write('0:01:0')
        pyautogui.press('tab')
        data = date.today()
        data = str(data)
        data = data.split('-')
        data.reverse()
        data = "/".join(data)
        pyautogui.write(data)
        pyautogui.press('tab')
        obs = "%s %s Ativo" % (documento, aluno)
        pyperclip.copy(obs)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('left')
        pyautogui.press('left')
        pyautogui.press('left')
        pyautogui.press('left')
