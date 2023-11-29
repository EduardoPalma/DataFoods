select i.id,i.name,im.id,im.name,im.grams from ingredient as i, ingredient_measure as im
                                          where i.id = im.ingredient_id;

select i.id,i.name,i.synonyms from ingredient as i;
