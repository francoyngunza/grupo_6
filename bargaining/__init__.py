from otree.api import *
import random


doc = """
Este juego de negociación implica a dos partes con intereses parcialmente contradictorios e información asimétrica. 
Un participante asumirá el rol de comprador y otro de vendedor. Si en el transcurso del juego no llegan a 
ningún acuerdo, entonces no recibirán pago alguno.
"""


class C(BaseConstants):
    NAME_IN_URL = 'bargaining'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    ENDOWMENT = cu(100)
    COMPRADOR_ROLE = 'comprador'
    VENDEDOR_ROLE = 'vendedor'
    

#establecemos dos roles, el comprador y el vendedor
    
class Subsession(BaseSubsession):

    def creating_session(subsession):
        subsession.group_randomly()

class Group(BaseGroup):

    oferta = models.CurrencyField(min=0, max=100, label="Por favor ingrese su oferta:")
    contraoferta = models.CurrencyField(min=0, max=100, label="Por favor ingrese su contraoferta:")
    
    acepta = models.IntegerField(
        choices=[[ 1, 'Sí'], [0, 'No']], 
        label="¿Acepta la contraoferta?",
        widget=widgets.RadioSelect,
        )
    
    valor_empresa = models.IntegerField()
    proporcion = models.FloatField()

class Player(BasePlayer):
    pago_final = models.CurrencyField()
    
    


# FUNCIONES

def set_payoffs(group):

    
    if group.acepta == 1:
       
       vendedor = group.get_player_by_role(C.VENDEDOR_ROLE)
       comprador = group.get_player_by_role(C.COMPRADOR_ROLE)
       valoracion_vendedor = group.valor_empresa * group.proporcion
       precio_aceptado = group.contraoferta
       vendedor.payoff = precio_aceptado - valoracion_vendedor
       comprador.payoff = group.valor_empresa - precio_aceptado

    else: 
       vendedor = group.get_player_by_role(C.VENDEDOR_ROLE)
       comprador = group.get_player_by_role(C.COMPRADOR_ROLE)
       vendedor.payoff = 0
       comprador.payoff = 0


def creating_session(player): 
    for p in player.get_groups(): 
            p.valor_empresa = random.choice([10, 15, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95])
            p.proporcion = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        



# PÁGINAS

class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Introduction (Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Oferta(Page):
    form_model = 'group'
    form_fields = ['oferta']
    timeout_seconds = 60

    @staticmethod
    def is_displayed(self:Player):
        return  self.role == C.VENDEDOR_ROLE
    
    def vars_for_templated (player):
        valor_empresa = random.choice([10, 15, 20,25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95])
        proporcion = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    

class Espera(WaitPage):
    pass


class Contraoferta(Page):
    form_model = 'group'
    form_fields = ['contraoferta'] 
    timeout_seconds = 60

    def vars_for_templated (player:Player):
        group = Oferta.group
        return dict (Oferta = group.oferta )
    
    @staticmethod                
    def is_displayed(self):
     return self.role == C.COMPRADOR_ROLE
    
    
class Espera(WaitPage):
    pass

class DecisionFinal(Page):
    form_model = 'group'
    form_fields = ['acepta']
    timeout_seconds = 60
   
    def vars_for_templated (player:Player):
        group = Contraoferta.group
        return dict (Contraoferta = group.acepta )
    
    @staticmethod                
    def is_displayed(self):
     return self.role == C.VENDEDOR_ROLE
    

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    
    @staticmethod 
    def vars_for_templated (player:Player):
        group = DecisionFinal.group
        return dict ( Oferta = group.oferta )
        

page_sequence = [Introduction, Instructions, Oferta, Espera, Contraoferta, Espera, DecisionFinal, ResultsWaitPage, Results]


