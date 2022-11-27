# atlas v1.0.2-ASYNC

Atlas is an website scanner, which
scans for:

Basic Host Info <br/>
Miss-configured Files <br/>
Dev Ports <br/>
Robots.txt <br/>

Thanks to (Leetcore) https://github.com/Leetcore
and his project ninja-hacker-cat
where I have the busting.txt from!

# 1.0.1 ==> 1.0.2-ASYNC

* Atlas is finally async
* I also removed some old code which made the scanner like 2x slower

# Installation

Clone the repo
```
git clone https://github.com/delltaxa/atlas.git
```

Direct in to the Directory
```
cd atlas/
```

One-Liner
```
git clone https://github.com/delltaxa/atlas.git; cd atlas/
```

# Usage

```
python3 main.py https://www.example.com/
```

or (If it's in /bin + named atlas + chmoded + and the busting.txt is in your directory)

```
atlas https://www.example.com/
```

That's it!

# Supports

Linux:   Yes <br/>
Windows: idk
