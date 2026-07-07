program a1;
var a,b:array [1..20] of integer;
    c,d:byte;
    e,f:integer;
begin
  for c := 1 to 20 do
  begin
    a[c] := random(100);
  end;
  e := a[1];
  for c := 2 to 20 do
  begin
    if(a[c] > e) then
    begin
      e := a[c];
    end;
  end;
  for d := 1 to 20 do
  begin
    b[d] := e;
  end;
  f := 0;
  for c := 1 to 20 do
  begin
    f := f + a[c];
  end;
  write('Массив Х: ');
  for c := 1 to 20 do
  begin
    write(a[c],' ');
  end;
  writeln('');
  write('Массив Y: ');
  for d := 1 to 20 do
  begin
    write(b[d],' ');
  end;
  writeln('');
  writeln('Сумма элементов массива Х: ',f);
end.