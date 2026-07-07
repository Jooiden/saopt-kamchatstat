program a1;
var a:array [1..100] of integer;
    b:byte;
    c,d:real;
    e:integer;
begin
  randomize;
  write('Сколько элементов? ');
  readln(e);
  write('Введите число t? ');
  readln(c);
  for b := 1 to e do
  begin
    a[b] := random(104) - 56;
  end;
  d := 1;
  for b := 1 to e do
  begin
    if((b mod 2 = 0) and (a[b] > c)) then
    begin
      d := d * a[b];
    end;
  end;
  for b := 1 to e do
  begin
    writeln(a[b]);
  end;
  writeln('Произведение элементов с чётными номерами, превосходящие число t= ',d);
end.
    