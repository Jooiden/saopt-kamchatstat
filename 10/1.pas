program a1;
var a:array [1..10] of integer;
    b,c:byte;
    d:integer;
begin
  randomize;
  write('Исходный массив: ');
  for b := 1 to 10 do
  begin
    a[b] := random(100);
    write(a[b]:3);
  end;
  writeln('');
  for b := 1 to 10 - 1 do
  begin
    for c := 1 to 10 - b do
    begin
      if(a[c] > a[c + 1]) then
      begin
        d := a[c];
        a[c] := a[c + 1];
        a[c + 1] := d;
      end;
    end;
  end;
  write('Отсортированный: ');
  for b := 1 to 10 do
  begin
    write(a[b]:3);
  end;
  writeln('');
end.