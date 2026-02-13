class Calculadora:
    
    def calcular(self, texInversion1, texInversion2, texInversion3, 
                       texInversion4, texInversion5, texInversion6, 
                       texInversion7,  texInversion8, texInversion9, texInversion10, 
                    texGananciaInv1, texGananciaInv2, texGananciaInv3,
                     texGananciaInv4, texGananciaInv5, texGananciaInv6,
                     texGananciaInv7, texGananciaInv8,  texGananciaInv9, 
                     texGananciaInv10,
                    texValorPersona1, texValorPersona2, texValorPersona3
                    , texValorPersona4):
        
        # Obtener textos de cada campo
        numInv1 = int(texInversion1);
        numInv2 = int(texInversion2);
        numInv3 = int(texInversion3);
        numInv4 = int(texInversion4);
        numInv5 = int(texInversion5);
        numInv6 = int(texInversion6);
        numInv7 = int(texInversion7);
        numInv8 = int(texInversion8);
        numInv9 = int(texInversion9);
        numInv10 = int(texInversion10);
        numGanInv1 = int(texGananciaInv1);
        numGanInv2 = int(texGananciaInv2);
        numGanInv3 = int(texGananciaInv3);
        numGanInv4 = int(texGananciaInv4);
        numGanInv5 = int(texGananciaInv5);
        numGanInv6 = int(texGananciaInv6);
        numGanInv7 = int(texGananciaInv7);
        numGanInv8 = int(texGananciaInv8);
        numGanInv9 = int(texGananciaInv9);
        numGanInv10 = int(texGananciaInv10);
        numValorPer1 = int(texValorPersona1);
        numValorPer2 = int(texValorPersona2);
        numValorPer3 = int(texValorPersona3);
        numValorPer4 = int(texValorPersona4);

        # Calculo Total Invertido
        totalAc = (numInv1 + numInv2 + numInv3 + numInv4 + numInv5 + numInv6 + numInv7 + numInv8 + numInv9 + numInv10);
        # Calculo Total Ganancias
        totalAcGan = (numGanInv1 + numGanInv2 + numGanInv3 + numGanInv4 + numGanInv5 + numGanInv6 + numGanInv7 + numGanInv8 + numGanInv9 + numGanInv10);
       
        # === PERSONA 1 ===
        # Calculo Porcentaje Persona 1
        PorcenPersona1 = ((numValorPer1*100)/totalAc);
        # Calculo Total Ganancia Persona 1
        GanPersona1 = ((PorcenPersona1*totalAcGan)/100);
        # Calculo Valor Próximo Persona 1
        ValorProximo1 = numValorPer1 + GanPersona1;
        # Calculo Restante después de Persona 1
        RestanteDespues1 = totalAc - numValorPer1;

        # === PERSONA 2 ===
        # Calculo Porcentaje Persona 2
        PorcenPersona2 = ((numValorPer2*100)/totalAc);
        # Calculo Total Ganancia Persona 2
        GanPersona2 = ((PorcenPersona2*totalAcGan)/100);
        # Calculo Valor Próximo Persona 2
        ValorProximo2 = numValorPer2 + GanPersona2;
        # Calculo Restante después de Persona 2
        RestanteDespues2 = RestanteDespues1 - numValorPer2;

        # === PERSONA 3 ===
        # Calculo Porcentaje Persona 3
        PorcenPersona3 = ((numValorPer3*100)/totalAc);
        # Calculo Total Ganancia Persona 3
        GanPersona3 = ((PorcenPersona3*totalAcGan)/100);
        # Calculo Valor Próximo Persona 3
        ValorProximo3 = numValorPer3 + GanPersona3;
        # Calculo Restante después de Persona 3
        RestanteDespues3 = RestanteDespues2 - numValorPer3;

        # === PERSONA 4 ===
        # Calculo Porcentaje Persona 4
        PorcenPersona4 = ((numValorPer4*100)/totalAc);
        # Calculo Total Ganancia Persona 4
        GanPersona4 = ((PorcenPersona4*totalAcGan)/100);
        # Calculo Valor Próximo Persona 4
        ValorProximo4 = numValorPer4 + GanPersona4;
        # Calculo Restante después de Persona 4
        RestanteDespues4 = RestanteDespues3 - numValorPer4;

        print(totalAcGan);
        return (totalAc, totalAcGan, 
                PorcenPersona1, GanPersona1, ValorProximo1, RestanteDespues1,
                PorcenPersona2, GanPersona2, ValorProximo2, RestanteDespues2,
                PorcenPersona3, GanPersona3, ValorProximo3, RestanteDespues3,
                PorcenPersona4, GanPersona4, ValorProximo4, RestanteDespues4)
