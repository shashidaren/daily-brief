(function(){
  try{
    const root=document.documentElement;
    const saved=localStorage.getItem('theme');
    const prefersLight=window.matchMedia('(prefers-color-scheme: light)').matches;
    if(saved==='light'||(!saved&&prefersLight)) root.classList.add('light');
    window.__toggleTheme=function(){
      root.classList.toggle('light');
      localStorage.setItem('theme', root.classList.contains('light')?'light':'dark');
    };
  }catch(e){}
})();