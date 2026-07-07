program a1;
var a:array [1..4,1..4] of integer;
    b,c:byte;
    d:integer;
begin
  for b := 1 to 4 do
  begin
    for c := 1 to 4 do
    begin
      a[b,c] := random(201) - 100;
    end;
  end;
  for b := 1 to 4 do
  begin
    for c := 1 to 4 do
    begin
      write(a[b,c],' ');
    end;
    writeln('');
  end;
  d := 0;
  for b := 2 to 5 do
  begin
    for c := 2 to 5 do
    begin
      if(b = c) then
      begin
        writeln(a[b - 1,c - 1]);
        d := d + a[b - 1,c - 1];
      end;
    end;
  end;
  writeln('Сумма главной диагонали массива = ',d);
end.