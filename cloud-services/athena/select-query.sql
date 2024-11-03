SELECT p.country,p.population,t.temperature,geo.east,geo.west,geo.north,geo.south FROM
    "default"."geolocation" as geo,
    "default"."population" as p,
    "default"."temperature" as t
WHERE p.country = t.country AND
      p.country = geo.country
      -- AND TRY(CAST(t.temperature AS double))  > 25
      -- AND TRY(CAST(t.temperature AS double))  < 10
LIMIT 10