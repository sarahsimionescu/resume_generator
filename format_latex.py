def format_experience(position: str, company: str, date: str, location: str, skills: list[str], points: list[str]) -> str:
    return r"\experienceSubheading{" + position + r"}{" + date + r"}{" + company + r"}{" + location + r"}{" + ", ".join(skills) + r"} \resumeItemListStart" + "\n".join([ r"\resumeItem {" + point + r"}" for point in points]) + r"\resumeItemListEnd"

def format_project(name: str, date: str, skills: list[str], points: list[str]) -> str:
    return r"\projectSubheading{" + name + r"}{" + date + r"}{" + ", ".join(skills) + r"} \resumeItemListStart" + "\n".join([ r"\resumeItem {" + point + r"}" for point in points]) + r"\resumeItemListEnd"


def format_link(name: str, link: str) -> str:
    return r'\href{' + link + r'}{\faExternalLink \space ' + name + r'}'

def format_latex(experiences : list[str], projects : list[str], skills : list[str]) -> str:
    return r"""
\documentclass[letterpaper,12pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{multicol}
\input{glyphtounicode}

\usepackage{baskervillef}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\RequirePackage{fontawesome}

\usepackage{geometry}
\geometry{portrait, margin=0.5in}

\pagestyle{fancy}
\fancyhf{} 
\fancyfoot{}
\setlength{\footskip}{10pt}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\linespread{0.9}
\setlist[itemize]{itemsep=2pt, topsep=1pt, partopsep=0pt}


\addtolength{\oddsidemargin}{0.0in}
\addtolength{\evensidemargin}{0.0in}
\addtolength{\textwidth}{0.0in}
\addtolength{\topmargin}{0.0in}
\addtolength{\textheight}{0.0in}




\urlstyle{same}

\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{\vspace{-6pt}
  \it
}{}{0em}{}[\color{black}\titlerule\vspace{-8pt}]

\pdfgentounicode=1



\newcommand{\resumeItem}[1]{
  \item{
    {\#1}
  }
}

\newlength{\daterangewidth}
\settowidth{\daterangewidth}{May, 2023 -- Present}

\newcommand{\experienceSubheading}[5]{
    \begin{tabularx}{\textwidth}{lXr}
      \textbf{\#1} @ \textit{\#3}, \textit{\#4} & & \#2 \\
    \end{tabularx}
    \vspace{-8pt}
}

\newcommand{\projectSubheading}[3]{
    \begin{tabularx}{\textwidth}{lXr}
      \textbf{\#1} | \textit{\#3} & & \#2 \\
    \end{tabularx}
    \vspace{-8pt}
}



\newcommand{\educationSubheading}[4]{
    \begin{tabularx}{\textwidth}{lXr}
      \textbf{\#1} @ \textit{\#3}, \textit{\#4} & & \#2 \\
    \end{tabularx}
    \vspace{-8pt}
}


\newcommand{\resumeSubItem}[1]{\resumeItem{\#1}}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeItemListStart}{\small\begin{itemize}[leftmargin=20pt]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{8pt}\normalsize}

\begin{document}
\fontfamily{lmss}\selectfont

\begin{center}
    {\LARGE \textbf{Nick Dritsakos}} \\ \vspace{5pt}

    \href{mailto://nikosdritsakoswork@gmail.com}{\large{\faExternalLink \space nikosdritsakoswork@gmail.com}}
    \href{https://www.linkedin.com/in/nikos-dritsakos/}{ \large{\faExternalLink \space in/nikos-dritsakos}}


\end{center}




""" + (r'\section{Experience}' if len(experiences) > 0 else "") + "\n".join(experiences) + r"""

\section{Education}

    \educationSubheading
        {First Class Honours Computer Science (BSc)}{Apr, 2024}
        {Brock University}{Niagara, ON}
        \resumeItemListStart
        \resumeItemAchieved Dean’s Honour List 3x, \textbf{one of 8 students} in the Faculty of Math and Science to have achieved this in
2024.
        

        

    \resumeItemListEnd


""" + (r'\section{Projects}' if len(projects) > 0 else "") + "\n".join(projects) + r"""


\section{Skills}

\begin{itemize}[leftmargin=0, label={}]
    \normalsize{\item{
     """ + ", ".join(skills) + r"""
      
    }}    
 \end{itemize}

\end{document}
"""