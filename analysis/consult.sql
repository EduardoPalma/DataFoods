select i.id,i.name,im.id,im.name,im.grams from ingredient as i, ingredient_measure as im
                                          where i.id = im.ingredient_id;