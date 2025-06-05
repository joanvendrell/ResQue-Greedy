# **ResQue-Greedy: Rewiring Sequential Greedy for Improved Submodular Maximization**

<div align="justify">
We introduce Rewired Sequential Greedy (ResQue Greedy), a novel approach that leverages the concept of submodular curvature as a risk measure within 
a lattice-based framework. By probabilistically identifying sub-optimal decisions through a fault-detection mechanism, ResQue Greedy implements a 
curvature-averse rewiring strategy. This strategy opportunistically redirects the solution path within the lattice, aiming to improve the approximation
performance without significantly increasing computational complexity. Numerical results demonstrate that ResQue Greedy achieves stronger near-optimality
bounds compared to the standard sequential greedy algorithm.
</div>

<img width="965" alt="lattice" src="https://github.com/user-attachments/assets/3264aa90-3b0e-4e7a-8eca-43058d4a116e" />


i.e. ResQue-Greedy applied for rovers landing allocation in Mars exploration for features extraction using DoMars16k dataset.

<img width="913" alt="mars3" src="https://github.com/user-attachments/assets/db53aee9-b403-4693-909a-100c9cdc3b48" />

If you find ResQue Greedy useful for your work, we kindly request that you cite the following [publication](https://arxiv.org/abs/2505.13670) :

```
@misc{JV-AK-SK:25,
  doi = {10.48550/ARXIV.2505.13670},
  url = {https://arxiv.org/abs/2505.13670},
  author = {Gallart,  Joan Vendrell and Kuhnle,  Alan and Kia,  Solmaz},
  keywords = {Discrete Mathematics (cs.DM),  Data Structures and Algorithms (cs.DS),  Optimization and Control (math.OC),  FOS: Computer and information sciences,  FOS: Computer and information sciences,  FOS: Mathematics,  FOS: Mathematics},
  title = {ResQue Greedy: Rewiring Sequential Greedy for Improved Submodular Maximization},
  publisher = {arXiv},
  year = {2025},
  copyright = {Creative Commons Attribution Non Commercial No Derivatives 4.0 International}
}
```
