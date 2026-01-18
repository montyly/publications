#!/usr/bin/env python3
"""
Generate README.md from talks.yaml

This script reads the talks.yaml file and generates the README.md
for the publications repository.

Usage:
    python generate_readme.py

The script expects talks.yaml to be in the same directory.
"""

import yaml
from pathlib import Path
from urllib.parse import quote


def make_link(text: str, path: str, base_url: str = "") -> str:
    """Create a markdown link, handling spaces in paths."""
    if path:
        # URL encode the path to handle spaces
        encoded_path = quote(path, safe='/')
        return f"[{text}]({base_url}{encoded_path})"
    return text


def generate_academic_conferences_table(conferences: list) -> str:
    """Generate the academic conferences markdown table."""
    lines = [
        "## Conferences\n",
        "| Paper | Conference | Authors |",
        "| --- | --- | --- |"
    ]
    
    for conf in conferences:
        title = conf['title']
        paper_link = make_link(title, conf.get('paper_path', ''))
        
        # Add slides link if available
        if conf.get('slides_path'):
            paper_link += f" ([slides]({quote(conf['slides_path'], safe='/')}))"
        
        lines.append(f"| {paper_link} | {conf['conference']} | {conf['authors']} |")
    
    return "\n".join(lines)


def generate_presentations_table(presentations: list) -> str:
    """Generate the industrial presentations markdown table."""
    lines = [
        "## Presentations\n",
        "| Title | Conference | Authors |",
        "| --- | --- | --- |"
    ]
    
    for pres in presentations:
        title = pres['title']
        
        # Create title with optional slides link
        if pres.get('slides_path'):
            title_cell = make_link(title, pres['slides_path'])
        else:
            title_cell = title
        
        # Add video link if available
        if pres.get('video_url'):
            title_cell += f" ([video]({pres['video_url']}))"
        
        # Add invited tag
        authors = pres['authors']
        if pres.get('invited'):
            authors += " (invited talk)"
        
        lines.append(f"| {title_cell} | {pres['conference']} | {authors} |")
    
    return "\n".join(lines)


def generate_workshops_table(workshops: list) -> str:
    """Generate the workshops markdown table."""
    lines = [
        "## Workshops\n",
        "| Title | Conference | Authors |",
        "| --- | --- | --- |"
    ]
    
    for ws in workshops:
        title = ws['title']
        
        # Create title with optional slides link
        if ws.get('slides_path'):
            title_cell = make_link(title, ws['slides_path'])
        else:
            title_cell = title
        
        # Add exercises link if available
        if ws.get('exercises_path'):
            title_cell += f" ([exercises]({quote(ws['exercises_path'], safe='/')}))"
        
        lines.append(f"| {title_cell} | {ws['conference']} | {ws['authors']} |")
    
    return "\n".join(lines)


def generate_podcasts_list(podcasts: list) -> str:
    """Generate the podcasts/panels markdown list."""
    lines = ["## Podcast, panel & misc\n"]
    
    for pod in podcasts:
        title = pod['title']
        url = pod.get('url', '')
        pod_type = pod['type']
        year = pod['year']
        event = pod.get('event', '')
        
        if url:
            entry = f"* [{title}]({url}) - {pod_type}"
        else:
            entry = f"* {title} - {pod_type}"
        
        if event:
            entry += f" ({event} - {year})"
        else:
            entry += f" ({year})"
        
        lines.append(entry)
    
    return "\n".join(lines)


def generate_readme(data: dict) -> str:
    """Generate the complete README.md content."""
    
    # Static header content
    header = """# Research projects contributions

| Project | Description | Role | Activity Period |
| --- | --- | --- | --- |
| [Tealer](https://github.com/crytic/tealer) | Static analysis framework for Algorand contracts | Project lead | 2020-present |
| [Slither](https://github.com/crytic/slither) | Static analysis framework for smart contracts | Project lead | 2018-present |
| [evm_cfg_builder](https://github.com/crytic/evm_cfg_builder) | Abstract interpreation based CFG recover for smart contract | Project lead | 2018-present |
| [Binsec](https://binsec.github.io/) | Symbolic execution for binaries | Development of a guided symbolic engine | 2015-2018 |
| [GUEB](https://github.com/montyly/gueb) | Use After Free detection on binary code | Project lead | 2013-2018 (unmaintained) |

# Academic

## PhD

* [Finding the needle in the heap : combining binary analysis techniques to trigger use-after-free](academic/thesis/thesis.pdf) (2017) - [Slides](academic/thesis/slides.pdf)

"""

    # Generate dynamic sections
    academic_conferences = generate_academic_conferences_table(data['academic_conferences'])
    
    # Static journals section
    journals = """
## Journals

| Paper | Journal | Authors |
| --- | --- | --- |
| [Statically detecting Use-After-Free on Binary Code](academic/journals/2014/JCVHT14/paper.pdf) | Journal of Computer Virology and Hacking Techniques 2014 | Josselin Feist, Laurent Mounier, Marie-Laure Potet |

## Program commitee

* [Workshop on Trusted Smart Contracts (WTSC)](https://fc22.ifca.ai/wtsc/index.html) 2021 - present
* [International Workshop on Smart Contract Analysis WoSCA](https://conf.researchr.org/track/issta-2020/issta-2020-wosca) - 2020 (co-chair)
* [Grehack](https://grehack.fr/) - 2015 (organizer), 2016

# Industrial

"""
    
    presentations = generate_presentations_table(data['industrial_presentations'])
    workshops = generate_workshops_table(data['industrial_workshops'])
    podcasts = generate_podcasts_list(data['podcasts_panels'])
    
    # Static blogposts section
    blogposts = """

## Technical Blogposts

### 2024

* [Evaluating blockchain security maturity](https://blog.trailofbits.com/2023/07/14/evaluating-blockchain-security-maturity/).

### 2020

* [Breaking Aave Upgradeability](https://blog.trailofbits.com/2020/12/16/breaking-aave-upgradeability/).
* [Good idea, bad design: How the Diamond standard falls short](https://blog.trailofbits.com/2020/10/30/good-idea-bad-design-how-the-diamond-standard-falls-short/)
* [Bug Hunting with Crytic](https://blog.trailofbits.com/2020/05/15/bug-hunting-with-crytic/)
* [Financial Cryptography 2020 Recap](https://blog.trailofbits.com/2020/03/18/financial-cryptography-2020-recap/)

### 2019

* [Watch Your Language: Our First Vyper Audit](https://blog.trailofbits.com/2019/10/24/watch-your-language-our-first-vyper-audit/)
* [Trail of Bits @ ICSE 2019 – Recap](https://blog.trailofbits.com/2019/06/19/trail-of-bits-icse-2019-recap/)
* [Slither: The Leading Static Analyzer for Smart Contracts](https://blog.trailofbits.com/2019/05/27/slither-the-leading-static-analyzer-for-smart-contracts/)

### 2018

* [How contract migration works](https://blog.trailofbits.com/2018/10/29/how-contract-migration-works/)
* [Contract upgrade anti-patterns](https://blog.trailofbits.com/2018/09/05/contract-upgrade-anti-patterns/)

### 2017

* [Hands on the Ethernaut CTF](https://blog.trailofbits.com/2017/11/06/hands-on-the-ethernaut-ctf/)
"""
    
    return header + academic_conferences + journals + presentations + "\n\n" + workshops + "\n\n" + podcasts + blogposts


def main():
    script_dir = Path(__file__).parent
    yaml_path = script_dir / "talks.yaml"
    readme_path = script_dir / "README.md"
    
    # Load YAML data
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Generate README
    readme_content = generate_readme(data)
    
    # Write README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Generated {readme_path}")


if __name__ == "__main__":
    main()
