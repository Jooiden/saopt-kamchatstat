program a1;
type matrix = array [1..10,1..10] of integer;
var a:matrix;
    b,c,d,e:byte;
    f:real;
procedure b1(var m:matrix);
var k,h,d,e:byte;
begin
  for d := 1 to b do
  begin
    for e := 1 to b do
    begin
      m[d,e] := random(10);
    end;
  end;
end;
procedure c1(var m:matrix);
var k,h,d,e:byte;
begin
  for d := 1 to b do
  begin
    for e := 1 to 10 do
    begin
      write(m[d,e]: 4);
    end;
    writeln(' ');
  end;
end;
begin
  writeln('Введите размерность матрицы: ');
  readln(b,c);
  b1(a);
  c1(a);
  f := 1;
  for d := 1 to b do
  begin
    for e := 1 to c do
    begin
      if(a[d,e] <> 0) then
      begin
        f := f * a[d,e];
      end;
    end;
  end;
  writeln('Произведение = ',f);
end.
