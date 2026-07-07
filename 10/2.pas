program a1;
var a:array [1..5] of char;
    b:array [1..6] of char;
    c:array [1..11] of char;
    d,e,f,g:byte;
    h:char;
begin
  randomize;
  for d := 1 to 5 do
  begin
    a[d] := Chr(Ord('A') + Random(26));
  end;
  for e := 1 to 6 do 
  begin
    b[e] := Chr(Ord('A') + random(26));
  end;
  for f := 1 to 5 do
  begin
    c[f] := a[f];
  end;
  for f := 1 to 6 do
  begin
    c[5 + f] := b[f];
  end;
  for f := 1 to 10 do
  begin
    for g := 1 to 11 - f do
    begin
      if(c[g] > c[g + 1]) then
      begin
        h := c[g];
        c[g] := c[g + 1];
        c[g + 1] := h;
      end;
    end;
  end;
  writeln('Массив А: ');
  for d := 1 to 5 do
  begin
    write(a[d],' ');
  end;
  writeln('');
  writeln('Массив B: ');
  for e := 1 to 6 do
  begin
    write(b[e],' ');
  end;
  writeln('');
  writeln('Массив C (отсортированный) : ');  
  for f := 1 to 11 do
  begin
    write(c[f],' ');
  end;
end.