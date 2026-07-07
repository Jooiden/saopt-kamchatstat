program a1;
var a:array [1..20] of integer;
    b:byte;
    c:integer;
begin
  randomize;
  for b := 1 to 20 do
  begin
    a[b] := random(201) - 100;
  end;
  c := 0;
  for b := 1 to 20 do
  begin
    if((a[b] < 0) and (a[b] mod 2 = 0)) then
    begin
      c := c + a[b];
    end;
  end;
  write('[');
  for b := 1 to 20 do
  begin
    write(a[b],' ');
  end;
  writeln(']');
  writeln('Сумма отриц. элементов = ',c);
end.