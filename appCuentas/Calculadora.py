class Calculadora:
    
    def activos(self, textcash, textSaving, textSaving2, textSaving3, textSaving4,
                textloan, textloan2, textloan3, textloan4, textOtherCurrency):
        
        print(textcash)
        # Obtener valores de cada campo
        num_cash = int(textcash)
        num_save = int(textSaving)
        num_save2 = int(textSaving2)
        num_save3 = int(textSaving3)
        num_save4 = int(textSaving4)
        num_loan = int(textloan)
        num_loan2 = int(textloan2)
        num_loan3 = int(textloan3)
        num_loan4 = int(textloan4)
        num_other_currency = int(textOtherCurrency)
        
        # Cálculo Total actual
        total_ac = (num_cash + num_save + num_save2 + num_save3 + num_save4 +
                    num_loan + num_loan2 + num_loan3 + num_loan4 + num_other_currency)
        
        return total_ac
    
    def patrimonio(self, textActivos, textDeudas):
        num_activos = int(textActivos)
        num_deudas = int(textDeudas)
        patrimonio = num_activos - num_deudas
        return patrimonio

    def sumaConsig(self, ca1, ca2, ca3, ca4):
        try:
            return float(ca1) + float(ca2) + float(ca3) + float(ca4)
        except ValueError:
            return "Error en los datos"
