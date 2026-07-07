program a1;
var a:array [1..4,1..5] of integer;
    b,c:byte;
    d:integer;
begin
  for b := 1 to 4 do 
  begin
    for c := 1 to 5 do
    begin
      a[b,c] := random(201) - 100;
    end;
  end;
  write('матрица [');
  for b := 1 to 4 do
  begin
    write('[');
    for c := 1 to 5 do
    begin
      if(c < 5) then
      begin
        write(a[b,c],',');
      end
      else
      begin
        write(a[b,c]);
      end;
    end;
    if(b < 4) then
    begin
      write('],');
    end
    else
    begin
      write(']');
    end;
  end;
  writeln(']');
  for b := 1 to 4 do
  begin
    d := 0;
    for c := 1 to 5 do
    begin
      if(a[b,c] >= 0) then
      begin
        d := d + 1;
      end;
    end;
    writeln('В ',b,' строке кол-во положительных элементов K= ',d);
  end;
end.