program a1;
var a:array [1..100] of integer;
    b:byte;
    c,d,e,f:integer;
begin
  write('Размер массива до 100 n=');
  readln(c);
  for b := 1 to c do
  begin
    a[b] := random(101) - 50;
  end;
  writeln('Исходный массив:');
  for b := 1 to c do
  begin
    write(a[b],' ');
  end;
  writeln('');
  d := 0;
  for b := 1 to c do
  begin
    if(a[b] > 0) then
    begin
      d := d + 1;
    end;
  end;
  e := 0;
  for b := 1 to c do
  begin
    if(a[b] < 0) then
    begin
      e := e + 1;
    end;
  end;
  f := abs(d - e);
  writeln('k=',f);
  if(f > 1) then
  begin
    if(d > e) then
    begin
      for b := 1 to c do
      begin
        if((d > e) and (a[b] > 0)) then
        begin
          a[b] := -1 * a[b];
          d := d - 1;
          e := e + 1;
        end;
      end;
    end
    else
    begin
      for b := 1 to c do
      begin
        if((d < e) and (a[b] < 0)) then
        begin
          a[b] := -1 * a[b];
          e := e - 1;
          d := d + 1;
        end;
      end;
    end;
    writeln('Массив после изменений:');
    for b := 1 to c do
    begin
      write(a[b],' ');
    end;
  end
  else
  begin
    writeln('Элементы не меняются');
  end;
  writeln('');
end.