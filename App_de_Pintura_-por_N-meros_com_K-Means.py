# Importando todas as coisas necessárias para o nosso programa funcionar.
# Esses são como os blocos de construção que vamos usar para fazer o nosso programa.

import numpy as np  # Esta é uma ferramenta para lidar com listas de números.
from sklearn.cluster import KMeans  # Essa é uma ferramenta que nos ajuda a encontrar grupos de coisas.
from sklearn.utils import shuffle  # Isso nos ajuda a misturar coisas.
import cv2  # Esta é uma ferramenta para trabalhar com imagens.
import streamlit as st  # Isso é o que nos permite criar a interface do nosso programa.
from PIL import Image  # Outra ferramenta para trabalhar com imagens.
import io  # Essa é uma ferramenta que nos ajuda a lidar com arquivos e dados.
import base64  # Essa é uma ferramenta que nos ajuda a converter dados.

cores_junguianas = {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'A cor preta representa a sombra do inconsciente, simbolizando os aspectos desconhecidos e reprimidos de uma pessoa.',
        'sombra': 'A cor preta é a própria sombra, representando os instintos primordiais e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor preta pode indicar uma personalidade enigmática, poderosa e misteriosa.',
        'diagnostico': 'O uso excessivo da cor preta pode indicar uma tendência à negatividade, depressão ou repressão emocional.'
    },
    '2': {
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'A cor branca simboliza a pureza, a iluminação e a verdade, representando o consciente em harmonia.',
        'sombra': 'A cor branca pode esconder aspectos de perfeccionismo e repressão de emoções negativas.',
        'personalidade': 'A cor branca indica uma personalidade que busca paz, clareza e simplicidade.',
        'diagnostico': 'O uso excessivo do branco pode indicar uma negação da escuridão e uma busca por perfeição inalcançável.'
    },
    '3': {
        'cor': 'Vermelho',
        'rgb': (255, 0, 0),
        'anima_animus': 'A cor vermelha representa paixão, energia e vida, simbolizando a força vital e o instinto.',
        'sombra': 'A cor vermelha pode esconder raiva, agressividade e impulsividade.',
        'personalidade': 'A cor vermelha indica uma personalidade vibrante, assertiva e cheia de vida.',
        'diagnostico': 'O uso excessivo do vermelho pode indicar tendências à agressividade, impaciência e comportamento impulsivo.'
    },
    '4': {
        'cor': 'Verde',
        'rgb': (0, 255, 0),
        'anima_animus': 'A cor verde simboliza crescimento, renovação e equilíbrio, representando a harmonia com a natureza.',
        'sombra': 'A cor verde pode esconder inveja, estagnação e resistência à mudança.',
        'personalidade': 'A cor verde indica uma personalidade calma, equilibrada e em harmonia com o ambiente.',
        'diagnostico': 'O uso excessivo do verde pode indicar resistência a mudanças, teimosia e tendência à estagnação.'
    },
    '5': {
        'cor': 'Azul',
        'rgb': (0, 0, 255),
        'anima_animus': 'A cor azul representa tranquilidade, sabedoria e confiança, simbolizando a mente consciente e a clareza.',
        'sombra': 'A cor azul pode esconder frieza emocional, distanciamento e falta de empatia.',
        'personalidade': 'A cor azul indica uma personalidade confiável, calma e intelectualmente orientada.',
        'diagnostico': 'O uso excessivo do azul pode indicar tendências à frieza emocional, distanciamento e falta de envolvimento.'
    },
    '6': {
        'cor': 'Amarelo',
        'rgb': (255, 255, 0),
        'anima_animus': 'A cor amarela simboliza otimismo, alegria e criatividade, representando a energia mental e a espontaneidade.',
        'sombra': 'A cor amarela pode esconder ansiedade, medo e superficialidade.',
        'personalidade': 'A cor amarela indica uma personalidade alegre, criativa e entusiasta.',
        'diagnostico': 'O uso excessivo do amarelo pode indicar tendências à ansiedade, inquietação e comportamento superficial.'
    },
    '7': {
        'cor': 'Laranja',
        'rgb': (255, 165, 0),
        'anima_animus': 'A cor laranja representa entusiasmo, excitação e vitalidade, simbolizando a sociabilidade e a alegria de viver.',
        'sombra': 'A cor laranja pode esconder superficialidade, falta de seriedade e comportamento extravagante.',
        'personalidade': 'A cor laranja indica uma personalidade extrovertida, entusiasta e calorosa.',
        'diagnostico': 'O uso excessivo do laranja pode indicar tendências à superficialidade, extravagância e falta de seriedade.'
    },
    '8': {
        'cor': 'Roxo',
        'rgb': (128, 0, 128),
        'anima_animus': 'A cor roxa simboliza espiritualidade, mistério e transformação, representando a conexão com o inconsciente e o divino.',
        'sombra': 'A cor roxa pode esconder sentimentos de superioridade, isolamento e escapismo.',
        'personalidade': 'A cor roxa indica uma personalidade intuitiva, espiritual e reflexiva.',
        'diagnostico': 'O uso excessivo do roxo pode indicar tendências ao escapismo, isolamento e sentimentos de superioridade.'
    },
    '9': {
        'cor': 'Rosa',
        'rgb': (255, 192, 203),
        'anima_animus': 'A cor rosa simboliza amor, compaixão e ternura, representando a conexão emocional e a gentileza.',
        'sombra': 'A cor rosa pode esconder ingenuidade, vulnerabilidade e falta de autoconfiança.',
        'personalidade': 'A cor rosa indica uma personalidade amorosa, carinhosa e gentil.',
        'diagnostico': 'O uso excessivo do rosa pode indicar tendências à ingenuidade, vulnerabilidade e dependência emocional.'
    },
    '10': {
        'cor': 'Marrom',
        'rgb': (165, 42, 42),
        'anima_animus': 'A cor marrom representa estabilidade, segurança e simplicidade, simbolizando a conexão com a terra e a realidade.',
        'sombra': 'A cor marrom pode esconder teimosia, conservadorismo e resistência à mudança.',
        'personalidade': 'A cor marrom indica uma personalidade prática, confiável e pé no chão.',
        'diagnostico': 'O uso excessivo do marrom pode indicar tendências à teimosia, conservadorismo e resistência à mudança.'
    },
    # Continuar adicionando as outras cores...
    '11': {
        'cor': 'Cinza',
        'rgb': (128, 128, 128),
        'anima_animus': 'A cor cinza simboliza neutralidade, equilíbrio e compromisso, representando a mediação entre extremos.',
        'sombra': 'A cor cinza pode esconder indecisão, falta de entusiasmo e apatia.',
        'personalidade': 'A cor cinza indica uma personalidade equilibrada, reservada e prática.',
        'diagnostico': 'O uso excessivo do cinza pode indicar tendências à indecisão, falta de entusiasmo e apatia.'
    },
    '12': {
        'cor': 'Turquesa',
        'rgb': (64, 224, 208),
        'anima_animus': 'A cor turquesa simboliza cura, proteção e comunicação, representando a paz interior e a clareza emocional.',
        'sombra': 'A cor turquesa pode esconder medo de mudança e isolamento emocional.',
        'personalidade': 'A cor turquesa indica uma personalidade serena, comunicativa e intuitiva.',
        'diagnostico': 'O uso excessivo do turquesa pode indicar tendências ao isolamento emocional e medo de mudança.'
    },
    '13': {
        'cor': 'Dourado',
        'rgb': (255, 215, 0),
        'anima_animus': 'A cor dourada simboliza riqueza, sucesso e iluminação, representando a realização e o poder espiritual.',
        'sombra': 'A cor dourada pode esconder arrogância, materialismo e superficialidade.',
        'personalidade': 'A cor dourada indica uma personalidade confiante, ambiciosa e iluminada.',
        'diagnostico': 'O uso excessivo do dourado pode indicar tendências à arrogância, materialismo e superficialidade.'
    },
    '14': {
        'cor': 'Prata',
        'rgb': (192, 192, 192),
        'anima_animus': 'A cor prata simboliza modernidade, inovação e prestígio, representando a intuição e a reflexão.',
        'sombra': 'A cor prata pode esconder frieza emocional, distanciamento e falta de empatia.',
        'personalidade': 'A cor prata indica uma personalidade sofisticada, inovadora e intuitiva.',
        'diagnostico': 'O uso excessivo do prata pode indicar tendências à frieza emocional e distanciamento.'
    },
    '15': {
        'cor': 'Vinho',
        'rgb': (128, 0, 0),
        'anima_animus': 'A cor vinho simboliza sofisticação, poder e mistério, representando a paixão madura e o controle emocional.',
        'sombra': 'A cor vinho pode esconder ressentimento, arrogância e comportamento controlador.',
        'personalidade': 'A cor vinho indica uma personalidade sofisticada, poderosa e misteriosa.',
        'diagnostico': 'O uso excessivo do vinho pode indicar tendências ao ressentimento, arrogância e comportamento controlador.'
    },
    '16': {
        'cor': 'Pêssego',
        'rgb': (255, 218, 185),
        'anima_animus': 'A cor pêssego simboliza ternura, carinho e aceitação, representando a suavidade e a compreensão.',
        'sombra': 'A cor pêssego pode esconder insegurança, indecisão e medo de rejeição.',
        'personalidade': 'A cor pêssego indica uma personalidade carinhosa, compreensiva e acolhedora.',
        'diagnostico': 'O uso excessivo do pêssego pode indicar tendências à insegurança, indecisão e medo de rejeição.'
    },
    '17': {
        'cor': 'Azeitona',
        'rgb': (128, 128, 0),
        'anima_animus': 'A cor azeitona simboliza paz, equilíbrio e sabedoria, representando a harmonia e a maturidade.',
        'sombra': 'A cor azeitona pode esconder teimosia, resistência à mudança e comportamento crítico.',
        'personalidade': 'A cor azeitona indica uma personalidade equilibrada, sábia e madura.',
        'diagnostico': 'O uso excessivo da cor azeitona pode indicar tendências à teimosia, resistência à mudança e comportamento crítico.'
    },
    '18': {
        'cor': 'Lavanda',
        'rgb': (230, 230, 250),
        'anima_animus': 'A cor lavanda simboliza tranquilidade, espiritualidade e cura, representando a serenidade e a introspecção.',
        'sombra': 'A cor lavanda pode esconder passividade, indecisão e escapismo.',
        'personalidade': 'A cor lavanda indica uma personalidade tranquila, espiritual e introspectiva.',
        'diagnostico': 'O uso excessivo da cor lavanda pode indicar tendências à passividade, indecisão e escapismo.'
    },
    '19': {
        'cor': 'Salmão',
        'rgb': (250, 128, 114),
        'anima_animus': 'A cor salmão simboliza aceitação, amor e calor, representando a harmonia emocional e a compreensão.',
        'sombra': 'A cor salmão pode esconder insegurança, medo de rejeição e comportamento dependente.',
        'personalidade': 'A cor salmão indica uma personalidade acolhedora, compreensiva e amorosa.',
        'diagnostico': 'O uso excessivo da cor salmão pode indicar tendências à insegurança, medo de rejeição e comportamento dependente.'
    },
    '20': {
        'cor': 'Ouro Velho',
        'rgb': (192, 192, 0),
        'anima_animus': 'A cor ouro velho simboliza tradição, valor e sabedoria, representando a estabilidade e a profundidade.',
        'sombra': 'A cor ouro velho pode esconder conservadorismo, teimosia e resistência à mudança.',
        'personalidade': 'A cor ouro velho indica uma personalidade estável, sábia e tradicional.',
        'diagnostico': 'O uso excessivo do ouro velho pode indicar tendências ao conservadorismo, teimosia e resistência à mudança.'
    },
    '21': {
        'cor': 'Champanhe',
        'rgb': (247, 231, 206),
        'anima_animus': 'A cor champanhe simboliza celebração, alegria e sofisticação, representando a leveza e o prazer.',
        'sombra': 'A cor champanhe pode esconder superficialidade, hedonismo e fuga da realidade.',
        'personalidade': 'A cor champanhe indica uma personalidade alegre, sofisticada e amante da vida.',
        'diagnostico': 'O uso excessivo da cor champanhe pode indicar tendências à superficialidade, hedonismo e fuga da realidade.'
    },
    '22': {
        'cor': 'Púrpura',
        'rgb': (128, 0, 128),
        'anima_animus': 'A cor púrpura simboliza realeza, poder e mistério, representando a dignidade e a introspecção.',
        'sombra': 'A cor púrpura pode esconder arrogância, distanciamento e comportamento autoritário.',
        'personalidade': 'A cor púrpura indica uma personalidade digna, poderosa e introspectiva.',
        'diagnostico': 'O uso excessivo do púrpura pode indicar tendências à arrogância, distanciamento e comportamento autoritário.'
    },
    '23': {
        'cor': 'Cobre',
        'rgb': (184, 115, 51),
        'anima_animus': 'A cor cobre simboliza criatividade, paixão e resistência, representando a vitalidade e a inovação.',
        'sombra': 'A cor cobre pode esconder teimosia, impulsividade e comportamento extravagante.',
        'personalidade': 'A cor cobre indica uma personalidade criativa, apaixonada e resistente.',
        'diagnostico': 'O uso excessivo da cor cobre pode indicar tendências à teimosia, impulsividade e comportamento extravagante.'
    },
    '24': {
        'cor': 'Bege',
        'rgb': (245, 245, 220),
        'anima_animus': 'A cor bege simboliza simplicidade, modéstia e naturalidade, representando a paz e a aceitação.',
        'sombra': 'A cor bege pode esconder passividade, falta de criatividade e conformismo.',
        'personalidade': 'A cor bege indica uma personalidade simples, modesta e natural.',
        'diagnostico': 'O uso excessivo da cor bege pode indicar tendências à passividade, falta de criatividade e conformismo.'
    },
    '25': {
        'cor': 'Creme',
        'rgb': (255, 253, 208),
        'anima_animus': 'A cor creme simboliza calma, pureza e suavidade, representando a paz interior e a simplicidade.',
        'sombra': 'A cor creme pode esconder passividade, indecisão e medo de conflito.',
        'personalidade': 'A cor creme indica uma personalidade calma, pura e suave.',
        'diagnostico': 'O uso excessivo da cor creme pode indicar tendências à passividade, indecisão e medo de conflito.'
    },
    '26': {
        'cor': 'Terracota',
        'rgb': (204, 78, 92),
        'anima_animus': 'A cor terracota simboliza força, resiliência e terra, representando a conexão com o mundo físico.',
        'sombra': 'A cor terracota pode esconder teimosia, resistência à mudança e comportamento rígido.',
        'personalidade': 'A cor terracota indica uma personalidade forte, resiliente e conectada à terra.',
        'diagnostico': 'O uso excessivo da cor terracota pode indicar tendências à teimosia, resistência à mudança e comportamento rígido.'
    },
    '27': {
        'cor': 'Caramelo',
        'rgb': (175, 111, 9),
        'anima_animus': 'A cor caramelo simboliza conforto, calor e doçura, representando a segurança e a aceitação.',
        'sombra': 'A cor caramelo pode esconder complacência, falta de ambição e comportamento passivo.',
        'personalidade': 'A cor caramelo indica uma personalidade confortável, calorosa e doce.',
        'diagnostico': 'O uso excessivo da cor caramelo pode indicar tendências à complacência, falta de ambição e comportamento passivo.'
    },
    '28': {
        'cor': 'Coral',
        'rgb': (255, 127, 80),
        'anima_animus': 'A cor coral simboliza energia, vitalidade e alegria, representando a espontaneidade e a paixão.',
        'sombra': 'A cor coral pode esconder impulsividade, superficialidade e comportamento imprudente.',
        'personalidade': 'A cor coral indica uma personalidade energética, vital e alegre.',
        'diagnostico': 'O uso excessivo da cor coral pode indicar tendências à impulsividade, superficialidade e comportamento imprudente.'
    },
    '29': {
        'cor': 'Verde Limão',
        'rgb': (50, 205, 50),
        'anima_animus': 'A cor verde limão simboliza frescor, juventude e vitalidade, representando a renovação e a energia.',
        'sombra': 'A cor verde limão pode esconder imaturidade, impulsividade e comportamento irresponsável.',
        'personalidade': 'A cor verde limão indica uma personalidade fresca, jovem e cheia de vida.',
        'diagnostico': 'O uso excessivo da cor verde limão pode indicar tendências à imaturidade, impulsividade e comportamento irresponsável.'
    },
    '30': {
        'cor': 'Lilás',
        'rgb': (200, 162, 200),
        'anima_animus': 'A cor lilás simboliza delicadeza, espiritualidade e transformação, representando a conexão com o divino.',
        'sombra': 'A cor lilás pode esconder escapismo, passividade e indecisão.',
        'personalidade': 'A cor lilás indica uma personalidade delicada, espiritual e transformadora.',
        'diagnostico': 'O uso excessivo da cor lilás pode indicar tendências ao escapismo, passividade e indecisão.'
    },
    '31': {
        'cor': 'Amêndoa',
        'rgb': (239, 222, 205),
        'anima_animus': 'A cor amêndoa simboliza gentileza, acolhimento e simplicidade, representando a aceitação e a compreensão.',
        'sombra': 'A cor amêndoa pode esconder insegurança, dependência emocional e falta de iniciativa.',
        'personalidade': 'A cor amêndoa indica uma personalidade gentil, acolhedora e simples.',
        'diagnostico': 'O uso excessivo da cor amêndoa pode indicar tendências à insegurança, dependência emocional e falta de iniciativa.'
    },
    '32': {
        'cor': 'Musgo',
        'rgb': (173, 223, 173),
        'anima_animus': 'A cor musgo simboliza estabilidade, natureza e crescimento, representando a conexão com a terra e a harmonia.',
        'sombra': 'A cor musgo pode esconder estagnação, resistência à mudança e comportamento conservador.',
        'personalidade': 'A cor musgo indica uma personalidade estável, conectada à natureza e em crescimento.',
        'diagnostico': 'O uso excessivo da cor musgo pode indicar tendências à estagnação, resistência à mudança e comportamento conservador.'
    },
    '33': {
        'cor': 'Cinza Claro',
        'rgb': (211, 211, 211),
        'anima_animus': 'A cor cinza claro simboliza neutralidade, equilíbrio e compromisso, representando a mediação entre extremos.',
        'sombra': 'A cor cinza claro pode esconder indecisão, falta de entusiasmo e apatia.',
        'personalidade': 'A cor cinza claro indica uma personalidade equilibrada, reservada e prática.',
        'diagnostico': 'O uso excessivo do cinza claro pode indicar tendências à indecisão, falta de entusiasmo e apatia.'
    },
    '34': {
        'cor': 'Ciano',
        'rgb': (0, 255, 255),
        'anima_animus': 'A cor ciano simboliza clareza, comunicação e tranquilidade, representando a paz e a serenidade.',
        'sombra': 'A cor ciano pode esconder frieza emocional, distanciamento e falta de empatia.',
        'personalidade': 'A cor ciano indica uma personalidade clara, comunicativa e tranquila.',
        'diagnostico': 'O uso excessivo da cor ciano pode indicar tendências à frieza emocional, distanciamento e falta de empatia.'
    },
    '35': {
        'cor': 'Magenta',
        'rgb': (255, 0, 255),
        'anima_animus': 'A cor magenta simboliza transformação, espiritualidade e criatividade, representando a conexão com o divino.',
        'sombra': 'A cor magenta pode esconder arrogância, distanciamento e comportamento autoritário.',
        'personalidade': 'A cor magenta indica uma personalidade transformadora, espiritual e criativa.',
        'diagnostico': 'O uso excessivo da cor magenta pode indicar tendências à arrogância, distanciamento e comportamento autoritário.'
    },
    '36': {
        'cor': 'Rubi',
        'rgb': (224, 17, 95),
        'anima_animus': 'A cor rubi simboliza paixão, energia e poder, representando a vitalidade e a intensidade emocional.',
        'sombra': 'A cor rubi pode esconder impulsividade, agressividade e comportamento dominador.',
        'personalidade': 'A cor rubi indica uma personalidade apaixonada, energética e poderosa.',
        'diagnostico': 'O uso excessivo da cor rubi pode indicar tendências à impulsividade, agressividade e comportamento dominador.'
    },
    '37': {
        'cor': 'Esmeralda',
        'rgb': (80, 200, 120),
        'anima_animus': 'A cor esmeralda simboliza renovação, equilíbrio e prosperidade, representando a harmonia e o crescimento.',
        'sombra': 'A cor esmeralda pode esconder inveja, estagnação e resistência à mudança.',
        'personalidade': 'A cor esmeralda indica uma personalidade renovada, equilibrada e próspera.',
        'diagnostico': 'O uso excessivo da cor esmeralda pode indicar tendências à inveja, estagnação e resistência à mudança.'
    },
    '38': {
        'cor': 'Bronze',
        'rgb': (205, 127, 50),
        'anima_animus': 'A cor bronze simboliza força, resistência e criatividade, representando a vitalidade e a inovação.',
        'sombra': 'A cor bronze pode esconder teimosia, impulsividade e comportamento extravagante.',
        'personalidade': 'A cor bronze indica uma personalidade forte, resistente e criativa.',
        'diagnostico': 'O uso excessivo da cor bronze pode indicar tendências à teimosia, impulsividade e comportamento extravagante.'
    },
    '39': {
        'cor': 'Ouro Rosa',
        'rgb': (255, 204, 204),
        'anima_animus': 'A cor ouro rosa simboliza amor, ternura e sofisticação, representando a beleza e a elegância.',
        'sombra': 'A cor ouro rosa pode esconder superficialidade, hedonismo e fuga da realidade.',
        'personalidade': 'A cor ouro rosa indica uma personalidade amorosa, terna e sofisticada.',
        'diagnostico': 'O uso excessivo da cor ouro rosa pode indicar tendências à superficialidade, hedonismo e fuga da realidade.'
    },
    '40': {
        'cor': 'Verde Água',
        'rgb': (127, 255, 212),
        'anima_animus': 'A cor verde água simboliza frescor, tranquilidade e renovação, representando a paz interior e a clareza emocional.',
        'sombra': 'A cor verde água pode esconder medo de mudança e isolamento emocional.',
        'personalidade': 'A cor verde água indica uma personalidade fresca, tranquila e renovada.',
        'diagnostico': 'O uso excessivo da cor verde água pode indicar tendências ao isolamento emocional e medo de mudança.'
    },
    '41': {
        'cor': 'Sépia',
        'rgb': (112, 66, 20),
        'anima_animus': 'A cor sépia simboliza tradição, estabilidade e memória, representando a conexão com o passado e a sabedoria.',
        'sombra': 'A cor sépia pode esconder conservadorismo, teimosia e resistência à mudança.',
        'personalidade': 'A cor sépia indica uma personalidade tradicional, estável e sábia.',
        'diagnostico': 'O uso excessivo da cor sépia pode indicar tendências ao conservadorismo, teimosia e resistência à mudança.'
    },
    '42': {
        'cor': 'Verde Musgo',
        'rgb': (0, 100, 0),
        'anima_animus': 'A cor verde musgo simboliza estabilidade, natureza e crescimento, representando a conexão com a terra e a harmonia.',
        'sombra': 'A cor verde musgo pode esconder estagnação, resistência à mudança e comportamento conservador.',
        'personalidade': 'A cor verde musgo indica uma personalidade estável, conectada à natureza e em crescimento.',
        'diagnostico': 'O uso excessivo da cor verde musgo pode indicar tendências à estagnação, resistência à mudança e comportamento conservador.'
    },
    '43': {
        'cor': 'Caqui',
        'rgb': (240, 230, 140),
        'anima_animus': 'A cor caqui simboliza simplicidade, naturalidade e calma, representando a paz e a aceitação.',
        'sombra': 'A cor caqui pode esconder passividade, falta de criatividade e conformismo.',
        'personalidade': 'A cor caqui indica uma personalidade simples, natural e calma.',
        'diagnostico': 'O uso excessivo da cor caqui pode indicar tendências à passividade, falta de criatividade e conformismo.'
    },
    '44': {
        'cor': 'Fúcsia',
        'rgb': (255, 0, 255),
        'anima_animus': 'A cor fúcsia simboliza transformação, espiritualidade e criatividade, representando a conexão com o divino.',
        'sombra': 'A cor fúcsia pode esconder arrogância, distanciamento e comportamento autoritário.',
        'personalidade': 'A cor fúcsia indica uma personalidade transformadora, espiritual e criativa.',
        'diagnostico': 'O uso excessivo da cor fúcsia pode indicar tendências à arrogância, distanciamento e comportamento autoritário.'
    },
    '45': {
        'cor': 'Marfim',
        'rgb': (255, 255, 240),
        'anima_animus': 'A cor marfim simboliza pureza, calma e elegância, representando a paz interior e a sofisticação.',
        'sombra': 'A cor marfim pode esconder passividade, indecisão e medo de conflito.',
        'personalidade': 'A cor marfim indica uma personalidade pura, calma e elegante.',
        'diagnostico': 'O uso excessivo da cor marfim pode indicar tendências à passividade, indecisão e medo de conflito.'
    },
    '46': {
        'cor': 'Limão',
        'rgb': (255, 250, 205),
        'anima_animus': 'A cor limão simboliza frescor, vitalidade e alegria, representando a renovação e a energia.',
        'sombra': 'A cor limão pode esconder imaturidade, impulsividade e comportamento irresponsável.',
        'personalidade': 'A cor limão indica uma personalidade fresca, vital e alegre.',
        'diagnostico': 'O uso excessivo da cor limão pode indicar tendências à imaturidade, impulsividade e comportamento irresponsável.'
    },
    '47': {
        'cor': 'Açafrão',
        'rgb': (244, 196, 48),
        'anima_animus': 'A cor açafrão simboliza energia, criatividade e alegria, representando a vitalidade e a inovação.',
        'sombra': 'A cor açafrão pode esconder impulsividade, superficialidade e comportamento imprudente.',
        'personalidade': 'A cor açafrão indica uma personalidade energética, criativa e alegre.',
        'diagnostico': 'O uso excessivo da cor açafrão pode indicar tendências à impulsividade, superficialidade e comportamento imprudente.'
    },
    '48': {
        'cor': 'Lavanda Claro',
        'rgb': (230, 230, 250),
        'anima_animus': 'A cor lavanda claro simboliza tranquilidade, espiritualidade e cura, representando a serenidade e a introspecção.',
        'sombra': 'A cor lavanda claro pode esconder passividade, indecisão e escapismo.',
        'personalidade': 'A cor lavanda claro indica uma personalidade tranquila, espiritual e introspectiva.',
        'diagnostico': 'O uso excessivo da cor lavanda claro pode indicar tendências à passividade, indecisão e escapismo.'
    },
    '49': {
        'cor': 'Dourado',
        'rgb': (255, 215, 0),
        'anima_animus': 'A cor dourado simboliza riqueza, poder e sucesso, representando a prosperidade e a ambição.',
        'sombra': 'A cor dourado pode esconder arrogância, materialismo e comportamento autoritário.',
        'personalidade': 'A cor dourado indica uma personalidade próspera, ambiciosa e poderosa.',
        'diagnostico': 'O uso excessivo da cor dourado pode indicar tendências à arrogância, materialismo e comportamento autoritário.'
    },
    '50': {
        'cor': 'Cinza Escuro',
        'rgb': (169, 169, 169),
        'anima_animus': 'A cor cinza escuro simboliza neutralidade, equilíbrio e compromisso, representando a mediação entre extremos.',
        'sombra': 'A cor cinza escuro pode esconder indecisão, falta de entusiasmo e apatia.',
        'personalidade': 'A cor cinza escuro indica uma personalidade equilibrada, reservada e prática.',
        'diagnostico': 'O uso excessivo do cinza escuro pode indicar tendências à indecisão, falta de entusiasmo e apatia.'
    },
    '51': {
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'A cor branca simboliza pureza, paz e clareza, representando a harmonia e a inocência.',
        'sombra': 'A cor branca pode esconder frieza emocional, distanciamento e falta de empatia.',
        'personalidade': 'A cor branca indica uma personalidade pura, pacífica e clara.',
        'diagnostico': 'O uso excessivo da cor branca pode indicar tendências à frieza emocional, distanciamento e falta de empatia.'
    },
    '52': {
        'cor': 'Prata',
        'rgb': (192, 192, 192),
        'anima_animus': 'A cor prata simboliza modernidade, inovação e sofisticação, representando a elegância e a adaptabilidade.',
        'sombra': 'A cor prata pode esconder superficialidade, hedonismo e fuga da realidade.',
        'personalidade': 'A cor prata indica uma personalidade moderna, inovadora e sofisticada.',
        'diagnostico': 'O uso excessivo da cor prata pode indicar tendências à superficialidade, hedonismo e fuga da realidade.'
    },
    '53': {
        'cor': 'Bronze Claro',
        'rgb': (205, 127, 50),
        'anima_animus': 'A cor bronze claro simboliza força, resistência e criatividade, representando a vitalidade e a inovação.',
        'sombra': 'A cor bronze claro pode esconder teimosia, impulsividade e comportamento extravagante.',
        'personalidade': 'A cor bronze claro indica uma personalidade forte, resistente e criativa.',
        'diagnostico': 'O uso excessivo da cor bronze claro pode indicar tendências à teimosia, impulsividade e comportamento extravagante.'
    },
    '54': {
        'cor': 'Cinza Médio',
        'rgb': (128, 128, 128),
        'anima_animus': 'A cor cinza médio simboliza neutralidade, equilíbrio e compromisso, representando a mediação entre extremos.',
        'sombra': 'A cor cinza médio pode esconder indecisão, falta de entusiasmo e apatia.',
        'personalidade': 'A cor cinza médio indica uma personalidade equilibrada, reservada e prática.',
        'diagnostico': 'O uso excessivo do cinza médio pode indicar tendências à indecisão, falta de entusiasmo e apatia.'
    },
    '55': {
        'cor': 'Verde Pastel',
        'rgb': (119, 221, 119),
        'anima_animus': 'A cor verde pastel simboliza frescor, tranquilidade e renovação, representando a paz interior e a clareza emocional.',
        'sombra': 'A cor verde pastel pode esconder medo de mudança e isolamento emocional.',
        'personalidade': 'A cor verde pastel indica uma personalidade fresca, tranquila e renovada.',
        'diagnostico': 'O uso excessivo da cor verde pastel pode indicar tendências ao isolamento emocional e medo de mudança.'
    },
    '56': {
        'cor': 'Azul Pastel',
        'rgb': (174, 198, 207),
        'anima_animus': 'A cor azul pastel simboliza calma, clareza e serenidade, representando a paz interior e a harmonia.',
        'sombra': 'A cor azul pastel pode esconder passividade, indecisão e medo de conflito.',
        'personalidade': 'A cor azul pastel indica uma personalidade calma, clara e serena.',
        'diagnostico': 'O uso excessivo da cor azul pastel pode indicar tendências à passividade, indecisão e medo de conflito.'
    },
    '57': {
        'cor': 'Rosa Pastel',
        'rgb': (255, 209, 220),
        'anima_animus': 'A cor rosa pastel simboliza ternura, carinho e aceitação, representando a suavidade e a compreensão.',
        'sombra': 'A cor rosa pastel pode esconder insegurança, indecisão e medo de rejeição.',
        'personalidade': 'A cor rosa pastel indica uma personalidade carinhosa, compreensiva e acolhedora.',
        'diagnostico': 'O uso excessivo da cor rosa pastel pode indicar tendências à insegurança, indecisão e medo de rejeição.'
    },
    '58': {
        'cor': 'Amarelo Pastel',
        'rgb': (253, 253, 150),
        'anima_animus': 'A cor amarelo pastel simboliza alegria, energia e clareza, representando a vitalidade e o otimismo.',
        'sombra': 'A cor amarelo pastel pode esconder imaturidade, impulsividade e comportamento irresponsável.',
        'personalidade': 'A cor amarelo pastel indica uma personalidade alegre, energética e clara.',
        'diagnostico': 'O uso excessivo da cor amarelo pastel pode indicar tendências à imaturidade, impulsividade e comportamento irresponsável.'
    },
    '59': {
        'cor': 'Pêssego Pastel',
        'rgb': (255, 218, 185),
        'anima_animus': 'A cor pêssego pastel simboliza ternura, carinho e aceitação, representando a suavidade e a compreensão.',
        'sombra': 'A cor pêssego pastel pode esconder insegurança, indecisão e medo de rejeição.',
        'personalidade': 'A cor pêssego pastel indica uma personalidade carinhosa, compreensiva e acolhedora.',
        'diagnostico': 'O uso excessivo da cor pêssego pastel pode indicar tendências à insegurança, indecisão e medo de rejeição.'
    },
    '60': {
        'cor': 'Lavanda Pastel',
        'rgb': (230, 230, 250),
        'anima_animus': 'A cor lavanda pastel simboliza tranquilidade, espiritualidade e cura, representando a serenidade e a introspecção.',
        'sombra': 'A cor lavanda pastel pode esconder passividade, indecisão e escapismo.',
        'personalidade': 'A cor lavanda pastel indica uma personalidade tranquila, espiritual e introspectiva.',
        'diagnostico': 'O uso excessivo da cor lavanda pastel pode indicar tendências à passividade, indecisão e escapismo.'
    },

    # ... (outras cores Junguianas)
}

# Aqui estamos criando uma nova ferramenta que chamamos de "Canvas".
# Isso nos ajuda a lidar com imagens e cores.

def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c, m, y, k

def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

def buscar_cor_proxima(rgb, cores_junguianas):
    distancias = []
    for cor_junguiana in cores_junguianas.values():
        cor_junguiana_rgb = cor_junguiana['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb) - np.array(cor_junguiana_rgb)) ** 2))
        distancias.append(distancia)
    cor_proxima_index = np.argmin(distancias)
    return cores_junguianas[str(cor_proxima_index + 1)]

class Canvas():
    def __init__(self, src, nb_color, pixel_size=4000):
        self.src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)  # Corrige a ordem dos canais de cor
        self.nb_color = nb_color
        self.tar_width = pixel_size
        self.colormap = []

    def generate(self):
        im_source = self.resize()
        clean_img = self.cleaning(im_source)
        width, height, depth = clean_img.shape
        clean_img = np.array(clean_img, dtype="uint8") / 255
        quantified_image, colors = self.quantification(clean_img)
        canvas = np.ones(quantified_image.shape[:2], dtype="uint8") * 255

        for ind, color in enumerate(colors):
            self.colormap.append([int(c * 255) for c in color])
            mask = cv2.inRange(quantified_image, color, color)
            cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for contour in cnts:
                _, _, width_ctr, height_ctr = cv2.boundingRect(contour)
                if width_ctr > 10 and height_ctr > 10 and cv2.contourArea(contour, True) < -100:
                    cv2.drawContours(canvas, [contour], -1, (0, 0, 0), 1)
                    txt_x, txt_y = contour[0][0]
                    cv2.putText(canvas, '{:d}'.format(ind + 1), (txt_x, txt_y + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return canvas, colors, quantified_image

    def resize(self):
        (height, width) = self.src.shape[:2]
        if height > width:  # modo retrato
            dim = (int(width * self.tar_width / float(height)), self.tar_width)
        else:
            dim = (self.tar_width, int(height * self.tar_width / float(width)))
        return cv2.resize(self.src, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture):
        clean_pic = cv2.fastNlMeansDenoisingColored(picture, None, 10, 10, 7, 21)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(clean_pic, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        return img_dilation

    def quantification(self, picture):
        width, height, depth = picture.shape
        flattened = np.reshape(picture, (width * height, depth))
        sample = shuffle(flattened)[:1000]
        kmeans = KMeans(n_clusters=self.nb_color).fit(sample)
        labels = kmeans.predict(flattened)
        new_img = self.recreate_image(kmeans.cluster_centers_, labels, width, height)
        return new_img, kmeans.cluster_centers_

    def recreate_image(self, codebook, labels, width, height):
        vfunc = lambda x: codebook[labels[x]]
        out = vfunc(np.arange(width * height))
        return np.resize(out, (width, height, codebook.shape[1]))

# Configurações da barra lateral
st.sidebar.title("Criação das Paletas de cores e Tela numerada")

# Separador
st.sidebar.write("---")

# Seção de Informações do Autor
st.sidebar.header("Informações do Autor")
st.sidebar.image("clube.png", use_column_width=True)
st.sidebar.write("Nome: Marcelo Claro")
st.sidebar.write("Email: marceloclaro@geomaker.org")
st.sidebar.write("WhatsApp: (88) 98158-7145")

# Separador
st.sidebar.write("---")

# Seção de Configurações
st.sidebar.header("Configurações da Aplicação")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "png"])
nb_color = st.sidebar.slider('Escolha o número de cores para pintar', min_value=1, max_value=100, value=2, step=1)
total_ml = st.sidebar.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)
pixel_size = st.sidebar.slider('Escolha o tamanho do pixel da pintura', min_value=500, max_value=8000, value=4000, step=100)

import numpy as np

# ...

if st.sidebar.button('Gerar'):
    if uploaded_file is not None:
        # Abrir a imagem diretamente do arquivo carregado
        pil_image = Image.open(uploaded_file)
        if 'dpi' in pil_image.info:
            dpi = pil_image.info['dpi']
            st.write(f'Resolução da imagem: {dpi} DPI')

            # Calcula a dimensão física de um pixel
            cm_per_inch = pixel_size
            cm_per_pixel = cm_per_inch / dpi[0]  # Supõe-se que a resolução seja a mesma em ambas as direções
            st.write(f'Tamanho de cada pixel: {cm_per_pixel:.4f} centímetros')

        # Converter pil_image em uma matriz NumPy
        src = np.array(pil_image)

        canvas = Canvas(src, nb_color, pixel_size)  # Use src aqui em vez de pil_image
        result, colors, segmented_image = canvas.generate()
        
        # O restante do código permanece inalterado

        
        # O restante do código permanece inalterado


    # Converter imagem segmentada para np.uint8
    segmented_image = (segmented_image * 255).astype(np.uint8)

    # Agora converta de BGR para RGB
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

    # Análise da Cor Dominante Junguiana
    st.image(segmented_image, caption='Imagem Segmentada', use_column_width=True)
    cor_dominante = buscar_cor_proxima(colors[0], cores_junguianas)
    st.write("---")
    st.image(result, caption='Imagem para pintar', use_column_width=True)
    st.write("---")

    st.subheader("Análise da Cor Dominante Junguiana")
    st.write(f"A cor dominante na paleta é {cor_dominante['cor']}.")
    st.write(f"Anima/Animus: {cor_dominante['anima_animus']}")
    st.write(f"Sombra: {cor_dominante['sombra']}")
    st.write(f"Personalidade: {cor_dominante['personalidade']}")
    st.write(f"Diagnóstico: {cor_dominante['diagnostico']}")
    # Separador
    st.write("---")

    # Mostrar paleta de cores

    for i, color in enumerate(colors):
        color_block = np.ones((50, 50, 3), np.uint8) * color[::-1]  # Cores em formato BGR
        st.image(color_block, caption=f'Cor {i+1}', width=50)

        # Cálculo das proporções das cores CMYK
        r, g, b = color
        c, m, y, k = rgb_to_cmyk(r, g, b)
        c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml)

        # Calcular a área da cor na imagem segmentada
        color_area = np.count_nonzero(np.all(segmented_image == color, axis=-1))
        total_area = segmented_image.shape[0] * segmented_image.shape[1]
        color_percentage = (color_area / total_area) * 100

        # Separador
        st.write("---")

        st.subheader("Sketching and concept development da paleta de cor")
        st.write(f"""
        PALETAS DE COR PARA: {total_ml:.2f} ml.

        A cor pode ser alcançada pela combinação das cores primárias do modelo CMYK, utilizando a seguinte dosagem:

        Ciano (Azul) (C): {c_ml:.2f} ml
        Magenta (Vermelho) (M): {m_ml:.2f} ml
        Amarelo (Y): {y_ml:.2f} ml
        Preto (K): {k_ml:.2f} ml

        """)
        cor_proxima = buscar_cor_proxima(color, cores_junguianas)
        st.write(f"      Cor Junguiana Mais Próxima: {cor_proxima['cor']}")
        st.write(f"      Anima/Animus: {cor_proxima['anima_animus']}")
        st.write(f"      Sombra: {cor_proxima['sombra']}")
        st.write(f"      Personalidade: {cor_proxima['personalidade']}")
        st.write(f"      Diagnóstico: {cor_proxima['diagnostico']}")

    result_bytes = cv2.imencode('.jpg', result)[1].tobytes()
    # Separador
    st.write("---")
    st.image(result, caption='Imagem para pintar', use_column_width=True)
    st.download_button(
        label="Baixar Imagem para pintar",
        data=result_bytes,
        file_name='result.jpg',
        mime='image/jpeg')


    segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
    segmented_image_bytes = cv2.imencode('.jpg', segmented_image_rgb)[1].tobytes()
    # Separador
    st.write("---")
     
    st.image(segmented_image, caption='Imagem Segmentada', use_column_width=True)
    st.download_button(
        label="Baixar imagem segmentada",
        data=segmented_image_bytes,
        file_name='segmented.jpg',
        mime='image/jpeg')
