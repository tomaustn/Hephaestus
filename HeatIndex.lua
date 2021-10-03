local getDangerRating = function(AirTemperature, RelativeHumidity)
    local c1 = -42.379;
    local c2 = 2.04901523;
    local c3 = 10.14333127;
    local c4 = -0.22475541;
    local c5 = -6.83783 * math.pow(10, 3);
    local c6 = -5.481717 * math.pow(10, -2);
    local c7 = 1.22874 * math.pow(10, -3);
    local c8 = 8.5282 * math.pow(10, -4);
    local c9 = -1.99 * math.pow(10, -6);
    local cf = 0;
    if((80 <= AirTemperature and AirTemperature <= 112) and  RelativeHumidity <= 13) then
        cf = -((13-RelativeHumidity)/4) * math.pow(((17-(AirTemperature-95))/17), 0.5);
    elseif((80 <= AirTemperature and AirTemperature <= 87) and RelativeHumidity > 85) then
        cf = 0.02*(RelativeHumidity-85)*(87-AirTemperature);
    end;
    
    local HeatIndex = c1 +
    c2 * AirTemperature +
    c3 * RelativeHumidity +
    c4 * AirTemperature * RelativeHumidity + 
    c5 * math.pow(AirTemperature, 2) +
    c6 * math.pow(RelativeHumidity, 2) + 
    c7 * math.pow(AirTemperature, 2)* RelativeHumidity + 
    c8 * AirTemperature * math.pow(RelativeHumidity, 2) + 
    c9 * math.pow(AirTemperature, 2) * math.pow(RelativeHumidity, 2) +
    cf;
    
    --// 10/4 = 2.5 
    --// meaning each section of risk (caution, extreme caution, danger, or extreme danger)
    --// have a limit of increments of 2.5
    --// caution = 0 to 2.5
    --// extreme caution = 2.5 to 5
    --// danger = 5 to 7.5
    --// extreme danger = 7.5 to 10
    if(HeatIndex >= 126) then
        return 10;
    end;
    if(HeatIndex <= 80) then
        return 0;
    end;
    local ret = ((HeatIndex-80)*100)/(126-80);
    return ret/10;
end;
