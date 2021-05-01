select sp.name as name, sp.number_of_seats, it.name
from specific_place sp
         inner join infrastructure_types it
                    on sp.type_id = it.id
where sp.number_of_seats > 500;


select a.name as artist_name, g.name as genre
from artist_genre ag
         left join artists a on ag.artist_id = a.id
         left join genres g on ag.genre_id = g.id
where g.name = 'Драма';

select a.name as artist_name, i.name as impressario_name
from artist_impressario ai
         left join artists a on ai.artist_id = a.id
         left join impressarios i on ai.impressarios_id = i.id
where i.name = 'Ольга Закористян';

select a.name as artist_name, g.name as genre
from (select artist_id, count(genre_id) from artist_genre ag group by artist_id having count(genre_id) > 1) ac
         left join artists a on ac.artist_id = a.id
         left join artist_genre ag on ag.artist_id = a.id
         left join genres g on g.id = ag.genre_id;



select a.name as artist_name, i.name as impressario_name
from artist_impressario ai
         left join artists a on ai.artist_id = a.id
         left join impressarios i on ai.impressarios_id = i.id
where a.name = 'Олексій Рубиков';

select se.name as event_name, o.name as organizator
from specific_event se
         left join organizers o on se.organizer_id = o.id
where se.date < '2021-08-19 15:00:00.000000'

select concurs.name as concurs_name, a.name as participant_name, cp.place as place
from (select id, name from specific_event where type_id = 3) concurs
         left join concurs_participants cp on concurs.id = cp.id_concurs
         left join artists a on cp.id_participant = a.id
where cp.place < 4
  AND cp.place > 0
  AND concurs.name = 'Сміх країни'
order by cp.place asc;

select se.name as event_name, place.name as place
from (select id, name from specific_place where name = 'Стадіон "Дінамо" ') place
         left join specific_event se on place.id = se.place_id;

select g.name as genre, i.name as impressario
from genres g
         right join impressarios i on g.id = i.genre_id
where g.name = 'Драма';


select distinct a.name
from (select id
      from specific_event
      where type_id = 3
        AND date > '2020-08-19 00:00:00.000000'
        AND date < '2022-08-19 16:00:00.000000') event
         left join concurs_participants cp on event.id = cp.id_concurs
         left join artists a on cp.id_participant = a.id;


select o.name as organizator, count(event.id)
from (select id, organizer_id
      from specific_event
      where date > '2020-08-19 00:00:00.000000'
        AND date < '2022-08-19 16:00:00.000000') event
         left join organizers o on event.organizer_id = o.id
group by o.name;


select sp.name as location, event.date as date_of_event, event.name as event_name
from (select id, place_id, name, date
      from specific_event
      where date > '2020-08-19'
        AND date < '2021-08-19') event
         left join specific_place sp on event.place_id = sp.id



