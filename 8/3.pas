program a1;
var a:array [1..100] of real;
    b,c,d:byte;
    e,f:real;
begin
  randomize;
  for b := 1 to 10 do
  begin
    a[b] := random(1000);
  end;
  for b := 1 to 10 do
  begin
    write(a[b],' ');
  end;
  writeln(' ');
  e := a[1];
  c := 1;
  for b := 2 to 10 do
  begin
    if(a[b] > e) then 
    begin
      e := a[b];
      c := b;
    end;
  end;
  f := a[1];
  d := 1;
  for b := 2 to 10 do
  begin
    if(a[b] < f) then 
    begin
      f := a[b];
      d := b;
    end;
  end;
  writeln('Max = ',e);
  writeln('position: ',c);
  writeln('Min = ',f);
  writeln('position: ',d);
end.