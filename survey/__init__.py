from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'encuesta'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='¿Cuál es su edad?', min=18, max=100)
    gender = models.StringField(
        choices=[['Masculino', 'Masculino'], ['Femenino', 'Femenino']],
        label='¿Cuál es su género?',
        widget=widgets.RadioSelect,
    )
    ocupacion = models.StringField(
        choices=[['Estudiante', 'Estudiante'], ['Egresado', 'Egresado']],
        label='¿Cuál es su ocupación?',
        widget=widgets.RadioSelect,
    )


    universidad = models.StringField(
         choices=[['UP', 'UP'], ['UDEP', 'UDEP'],['PUCP', 'PUCP'],['UNMSM', 'UNMSM'],['UPC', 'UPC'],['U de Lima', 'U de Lima'],['UNTRM', 'UNTRM'],['ESAN', 'ESAN'],['UNPRG', 'UNPRG']],
        label='¿En qué universidad estudia?'
    )

    opcional = models.StringField(
        choices=[['Sí', 'Sí'],['No', 'No'], ['Prefiero no decirlo', 'Prefiero no decirlo']],
        label='¿Crees que eljuego fue justo?',

    )

    opcional2 = models.StringField(
        choices=[['Sí', 'Sí'],['No', 'No'], ['Prefiero no decirlo', 'Prefiero no decirlo']],
        label='¿El juego superó tus expectativas?',

    )
   
    opcional_3 = models.StringField(
        choices=[['Sí', 'Sí'],['No', 'No'], ['Tal vez', 'Tal vez']],
        label='¿Le recomendarías a un amigo que participe en el juego?',

    )
   
# FUNCTIONS
# PAGES 

class Survey1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender','ocupacion', 'universidad', 'opcional','opcional2','opcional_3' ]

 
class Agradecimientos(Page):
    pass
    

page_sequence = [Survey1, Agradecimientos]
