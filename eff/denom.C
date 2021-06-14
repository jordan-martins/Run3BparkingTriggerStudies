{ 
  TFile f("root/genstudy_pt.root");
  TTree* t = (TTree*)f.Get("tree");
  std::cout << "entries: " << t->GetEntries() << std::endl;
  TH2F denom("denom","denom",10, 0. ,10.,10, 0. ,10. );
  //int n = tree->Draw("gen_e1_pt:gen_e2_pt>>denom","singleMu3==1","goff");
  int n = tree->Draw("gen_e1_pt:gen_e2_pt>>denom","","goff");
  std::cout << "processed: " << n << std::endl;
  TFile fw("root/denom.root","RECREATE");
  denom.Write();
  fw.Close();
}
