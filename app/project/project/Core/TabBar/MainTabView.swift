//
//  MainTabView.swift
//  project
//
//  Created by Drew S on 2/27/24.
//

import SwiftUI

struct MainTabView: View {
    init() {
            // Customize the appearance of the tab bar
            UITabBar.appearance().barTintColor = UIColor.black
            UITabBar.appearance().isTranslucent = true
        }
    
    @State private var selectedTab = 0
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    VStack {
                        Image(systemName: selectedTab == 0 ? "house.fill" : "house")
                            .environment(\.symbolVariants,selectedTab == 0 ? .fill: .none)
                        Text("Home")
                    }
                }
                .onAppear{ selectedTab = 0}
                .tag(0)
            
            Text("Search")
                .tabItem {
                    VStack {
                        Image(systemName: "magnifyingglass")
                        Text("Search")
                    }
                }
                .onAppear{ selectedTab = 1}
                .tag(1)
            
            Text("Recipes")
                .tabItem {
                    VStack {
                        Image(systemName: selectedTab == 2 ?  "refrigerator.fill" : "refrigerator")
                            .environment(\.symbolVariants,selectedTab == 2 ? .fill: .none)
                        Text("Recipes")
                    }
                }
                .onAppear{ selectedTab = 2}
                .tag(2)
        }
    }
}

#Preview {
    MainTabView()
}
