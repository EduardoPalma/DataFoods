select i.id,i.name,im.id,im.name,im.grams from ingredient as i, ingredient_measure as im
                                          where i.id = im.ingredient_id;

select i.id,i.name,isy.name from ingredient as i, ingredient_synonym as isy where i.id = isy.ingredient_id;