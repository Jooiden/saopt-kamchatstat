program a1;
var a:array [1..50] of real;
    b:byte;
begin
  randomize;
  for b := 1 to 50 do
  begin
    a[b] := random(201) - 100;
  end;
  for b := 1 to 50 do
  begin
    if(a[b] >= 0) then
    begin
      write(a[b],' ');
    end;
  end;
  writeln(' ');
  writeln('Вывод массива');
  write('[');
  for b := 1 to 50 do
  begin
    write(a[b],' ');
  end;
  writeln(']');
end.