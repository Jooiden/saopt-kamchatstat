program a1;
var a:array[1..10] of integer;
    b:byte;
    c,d,e:integer;
begin
  for b := 1 to 10 do
  begin
    readln(a[b]);
  end;
  for b := 1 to 10 do
  begin
    write(a[b],' ');
  end;
  writeln(' ');
  c := 0;
  b := 2;
  while(b <= 10) do
  begin
    if(a[b] = a[b - 1]) then
    begin
      d := 1;
      e := b;
      while((e <= 10) and (a[e] = a[e - 1])) do
      begin
        d := d + 1;
        e := e + 1;
      end;
      if(d > c) then
      begin
        c := d;
        d := 1;
      end;
      b := b + d;
    end
    else
    begin
      b := b + 1;
    end;
  end;
  writeln(c);
end.