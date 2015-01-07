<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns:xi="http://www.w3.org/2003/XInclude" xmlns="http://www.w3.org/1999/xhtml"$if(lang)$ lang="$lang$"$endif$>
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <title>$title.main$</title>
  <style type="text/css">code{white-space: pre;}</style>
$if(highlighting-css)$
  <style type="text/css">
$highlighting-css$
  </style>
$endif$
$for(css)$
  <link rel="stylesheet" href="$css$" />
$endfor$
$if(math)$
  $math$
$endif$
$for(header-includes)$
  $header-includes$
$endfor$
$if(cssextra)$
  <link rel="stylesheet" href="$cssextra$" />
$endif$
</head>
<body>
$for(include-before)$
$include-before$
$endfor$
<p class="tl-content">
$author.name1$<br/>$author.name2$<br />$author.name3$
</p>
<p class="tm-content">
$title.main$<br/>$title.sub1$<br/>$title.sub2$
</p>
<p class="tr-content">
$revision.doc$<br/>rev. $revision.level$ / $revision.date$<br/><span class="tr-page"></span>
</p> 
$body$
$for(include-after)$
$include-after$
$endfor$
</body>
</html>
